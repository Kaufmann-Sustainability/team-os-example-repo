#!/usr/bin/env python3
"""Erzeugt eine eigenständige, interaktive HTML-Visualisierung des Objektgraphen.

Force-Directed-Graph (Vanilla-JS, kein CDN): Objekte = Punkte, Beziehungen = Kanten,
Cluster über Verbindungen + Gruppen-Gravitation (Farbe = ESRS-Standard bzw. Typ).
Ziehen, Zoomen, Pan, Hover-Tooltip.

Aufruf:  python3 tools/graph_html.py   ->  diagrams/graph.html
Benötigt: PyYAML.
"""
from __future__ import annotations
import re, sys, json, html
from pathlib import Path
try:
    import yaml
except ImportError:
    sys.exit("PyYAML benötigt")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "diagrams"; OUT.mkdir(exist_ok=True)
FM = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
VOCAB = {"has_target","has_kpi","has_initiative","has_iro","measured_by","supported_by",
         "approved_by","supports","at_risk_from","has_budget","uses_factor","concerns",
         "informed_by","backs","covers","discloses","reports","plans","applies","challenges"}
# Hub-Kanten (verbinden alles -> Hairball) weggelassen: scored_under, affects, based_on, decided_by


def load():
    objs = {}
    for p in (ROOT / "objects").glob("*.md"):
        txt = p.read_text(encoding="utf-8")
        m = FM.search(txt)
        if m:
            d = yaml.safe_load(m.group(1)) or {}
            h = re.search(r"(?m)^#\s+(.+)", txt)
            d["_h"] = h.group(1).strip() if h else ""
            objs[d.get("id", p.stem)] = d
    return objs


def grp(o):
    e = str(o.get("esrs_bezug") or "")
    m = re.match(r"(ESRS|ES|E\d|S\d|G\d)", e)
    return m.group(1) if m else str(o.get("type"))


def lst(v):
    return v if isinstance(v, list) else [v] if v else []


def main():
    objs = load()
    ids = set(objs)
    # Kanten (ungerichtet, dedupliziert)
    seen, links = set(), []
    for oid, o in objs.items():
        for rel in VOCAB:
            for t in lst(o.get(rel)):
                if t in ids:
                    key = tuple(sorted((oid, t)))
                    if key not in seen:
                        seen.add(key); links.append({"s": key[0], "t": key[1]})
    deg = {i: 0 for i in ids}
    for l in links:
        deg[l["s"]] += 1; deg[l["t"]] += 1

    groups = sorted({grp(o) for o in objs.values()})
    nodes = []
    for oid, o in objs.items():
        label = o.get("_h") or oid
        title = f"{oid}  ·  {o.get('type')}"
        if o.get("esrs_bezug"): title += f"  ·  {o['esrs_bezug']}"
        if o.get("type") == "iro":
            title += f"  ·  Impact {o.get('impact_score','?')} / Financial {o.get('financial_score','?')}  ·  wesentlich={str(o.get('wesentlich')).strip(chr(34))}"
        if o.get("type") == "target":
            title += f"  ·  {o.get('baseline_wert')}→{o.get('zielwert')} {o.get('einheit','')}"
        nodes.append({"id": oid, "t": o.get("type"), "g": grp(o), "d": deg[oid],
                      "l": str(label)[:30], "title": title,
                      "mat": str(o.get("wesentlich")).strip('"').lower() != "nein"})

    types = sorted({n["t"] for n in nodes})
    data = {"nodes": nodes, "links": links, "groups": groups, "types": types}
    n_obj, n_edge = len(nodes), len(links)
    title = f"{ROOT.name} — Objektgraph"
    sub = (f"{n_obj} Objekte · {n_edge} Kanten · Farbe = Objektklasse (Topic/IRO/Ziel/KPI/Policy/Initiative…) · "
           f"KLICK auf einen Knoten = nur dessen Umfeld zeigen (Klick auf Hintergrund = zurück) · ziehen · scroll=zoom · hover=Details")
    htmldoc = TEMPLATE.replace("__DATA__", json.dumps(data)).replace("__TITLE__", html.escape(title)).replace("__SUB__", html.escape(sub))
    (OUT / "graph.html").write_text(htmldoc, encoding="utf-8")
    print(f"Gerendert: diagrams/graph.html  ({n_obj} Objekte, {n_edge} Kanten, {len(groups)} Gruppen)")


TEMPLATE = r"""<!DOCTYPE html><html lang="de"><head><meta charset="utf-8">
<title>__TITLE__</title><style>
html,body{margin:0;height:100%;background:#0f1419;color:#e6edf3;font-family:Helvetica,Arial,sans-serif;overflow:hidden}
#h{position:fixed;top:0;left:0;right:0;padding:10px 14px;z-index:5;pointer-events:none}
#h b{font-size:17px}#h span{font-size:12px;color:#9aa7b4}
#legend{position:fixed;top:54px;left:14px;z-index:5;font-size:12px;max-width:160px}
#legend div{margin:2px 0;cursor:default}
#legend i{display:inline-block;width:11px;height:11px;border-radius:50%;margin-right:6px;vertical-align:-1px}
#tip{position:fixed;display:none;background:#1c2430;border:1px solid #30363d;padding:6px 9px;border-radius:6px;
font-size:12px;pointer-events:none;z-index:9;max-width:340px}
canvas{display:block}
</style></head><body>
<div id="h"><b>__TITLE__</b><br><span>__SUB__</span></div>
<div id="legend"></div><div id="tip"></div>
<canvas id="c"></canvas>
<script>
const DATA = __DATA__;
const PALETTE=["#e74c3c","#e67e22","#f1c40f","#2ecc71","#1abc9c","#3498db","#9b59b6","#e84393",
"#00cec9","#fd79a8","#a29bfe","#fab1a0","#55efc4","#74b9ff","#ffeaa7"];
const cv=document.getElementById('c'),ctx=cv.getContext('2d'),tip=document.getElementById('tip');
let W,H;function resize(){W=cv.width=innerWidth;H=cv.height=innerHeight;}resize();addEventListener('resize',resize);
const N=DATA.nodes,L=DATA.links,G=DATA.groups;
const T=DATA.types;
const TYPECOL={topic:"#3498db",iro:"#e67e22",target:"#2ecc71",kpi:"#1abc9c",policy:"#9b59b6",
initiative:"#e74c3c",dependency:"#95a5a6",decision:"#f1c40f",methodology:"#e84393",person:"#7f8c8d",
"audit-finding":"#c0392b",finding:"#d35400",disclosure:"#2980b9",datapoint:"#636e72",evidence:"#8395a7",
control:"#576574",budget:"#27ae60","emission-factor":"#16a085",term:"#a29bfe",threshold:"#fd79a8",
stakeholder:"#fdcb6e","annual-plan":"#00cec9",strategy:"#0c5fb3"};
function tcol(t){return TYPECOL[t]||"#bbb";}
const cx=()=>W/2,cy=()=>H/2,Rr=()=>Math.min(W,H)*0.36;
const anchor={};G.forEach((g,i)=>{const a=2*Math.PI*i/G.length;anchor[g]=[()=>cx()+Rr()*Math.cos(a),()=>cy()+Rr()*Math.sin(a)];});
const byId={};N.forEach(n=>{byId[n.id]=n;const[ax,ay]=anchor[n.g];n.x=ax()+(Math.random()-.5)*140;n.y=ay()+(Math.random()-.5)*140;n.vx=0;n.vy=0;n.r=3+Math.sqrt(n.d)*1.4;});
// Legende
const lg=document.getElementById('legend');T.forEach(t=>{const d=document.createElement('div');
d.innerHTML='<i style="background:'+tcol(t)+'"></i>'+t;lg.appendChild(d);});
const REP=900,LEN=34,SPR=0.025,GG=0.012,CG=0.0018,DAMP=0.84;let alpha=1;
function tick(){
 for(let i=0;i<N.length;i++){const a=N[i];for(let j=i+1;j<N.length;j++){const b=N[j];
  let dx=a.x-b.x,dy=a.y-b.y,d2=dx*dx+dy*dy+0.01;if(d2>90000)continue;
  let d=Math.sqrt(d2),f=REP/d2,fx=f*dx/d,fy=f*dy/d;a.vx+=fx;a.vy+=fy;b.vx-=fx;b.vy-=fy;}}
 L.forEach(l=>{const a=byId[l.s],b=byId[l.t];let dx=b.x-a.x,dy=b.y-a.y,d=Math.sqrt(dx*dx+dy*dy)+.01;
  let f=(d-LEN)*SPR,fx=f*dx/d,fy=f*dy/d;a.vx+=fx;a.vy+=fy;b.vx-=fx;b.vy-=fy;});
 N.forEach(n=>{const[ax,ay]=anchor[n.g];n.vx+=(ax()-n.x)*GG+(cx()-n.x)*CG;n.vy+=(ay()-n.y)*GG+(cy()-n.y)*CG;
  if(n.fix||n.pin)return;n.vx*=DAMP;n.vy*=DAMP;n.x+=n.vx*alpha;n.y+=n.vy*alpha;});
 if(alpha>0.06)alpha*=0.996;
}
let scale=0.85,tx=0,ty=0;
let focusId=null,focusSet=null;
function vis(n){return !focusSet||focusSet.has(n.id);}
function draw(){
 ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,W,H);
 ctx.setTransform(scale,0,0,scale,tx,ty);
 ctx.strokeStyle=focusSet?"rgba(150,170,190,0.35)":"rgba(120,140,160,0.14)";ctx.lineWidth=0.7;ctx.beginPath();
 L.forEach(l=>{if(focusSet&&!(focusSet.has(l.s)&&focusSet.has(l.t)))return;
  const a=byId[l.s],b=byId[l.t];ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);});ctx.stroke();
 N.forEach(n=>{if(!vis(n))return;ctx.beginPath();ctx.arc(n.x,n.y,n.r,0,6.283);ctx.fillStyle=tcol(n.t);
  ctx.globalAlpha=n.mat?1:0.45;ctx.fill();ctx.globalAlpha=1;
  if(n.r>6||focusSet){ctx.strokeStyle=(n.id===focusId)?"#fff":"rgba(255,255,255,0.6)";
   ctx.lineWidth=(n.id===focusId)?2:0.8;ctx.stroke();}});
 ctx.fillStyle="#dbe4ee";ctx.font="10px Helvetica";
 N.forEach(n=>{if(!vis(n))return;if(focusSet||n.r>7){ctx.fillText(n.l,n.x+n.r+3,n.y+3);}});
}
function loop(){tick();draw();requestAnimationFrame(loop);}loop();
// Interaktion
function world(e){return[(e.clientX-tx)/scale,(e.clientY-ty)/scale];}
function pick(e){const[mx,my]=world(e);let best=null,bd=1e9;N.forEach(n=>{if(!vis(n))return;
 const d=(n.x-mx)**2+(n.y-my)**2;if(d<bd&&d<Math.max(80,n.r*n.r*4)){bd=d;best=n;}});return best;}
function neigh(id){const s=new Set([id]);L.forEach(l=>{if(l.s===id)s.add(l.t);if(l.t===id)s.add(l.s);});return s;}
function setFocus(id){
 if(focusId===id){clearFocus();return;}
 if(focusSet)focusSet.forEach(x=>byId[x].pin=false);
 focusId=id;focusSet=neigh(id);const f=byId[id];
 f.x=(W/2-tx)/scale;f.y=(H/2-ty)/scale;f.vx=f.vy=0;
 const nb=[...focusSet].filter(x=>x!==id),R=140;
 nb.forEach((x,i)=>{const a=2*Math.PI*i/nb.length,n=byId[x];n.x=f.x+R*Math.cos(a);n.y=f.y+R*Math.sin(a);n.vx=n.vy=0;});
 focusSet.forEach(x=>byId[x].pin=true);
}
function clearFocus(){if(focusSet)focusSet.forEach(x=>byId[x].pin=false);focusId=null;focusSet=null;}
let drag=null,pan=null,down=null;
cv.addEventListener('mousedown',e=>{const n=pick(e);down={n:n,x:e.clientX,y:e.clientY,m:false};
 if(n){drag=n;n.fix=true;}else{pan=[e.clientX-tx,e.clientY-ty];}});
addEventListener('mousemove',e=>{
 if(down&&(Math.abs(e.clientX-down.x)>4||Math.abs(e.clientY-down.y)>4))down.m=true;
 if(drag){const[mx,my]=world(e);drag.x=mx;drag.y=my;drag.vx=drag.vy=0;alpha=Math.max(alpha,0.3);}
 else if(pan){tx=e.clientX-pan[0];ty=e.clientY-pan[1];}
 else{const n=pick(e);if(n){tip.style.display='block';tip.style.left=(e.clientX+12)+'px';tip.style.top=(e.clientY+12)+'px';tip.textContent=n.title;}else tip.style.display='none';}
});
addEventListener('mouseup',()=>{
 if(down&&!down.m){if(down.n)setFocus(down.n.id);else clearFocus();}
 if(drag)drag.fix=false;drag=null;pan=null;down=null;});
cv.addEventListener('wheel',e=>{e.preventDefault();const f=e.deltaY<0?1.1:0.9;const mx=e.clientX,my=e.clientY;
 tx=mx-(mx-tx)*f;ty=my-(my-ty)*f;scale*=f;},{passive:false});
</script></body></html>"""

if __name__ == "__main__":
    main()
