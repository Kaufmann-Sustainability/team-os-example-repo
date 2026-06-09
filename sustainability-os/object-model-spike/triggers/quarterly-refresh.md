# Trigger: Quartalsweiser Refresh-Sweep

> **Antwort auf die Frage:** „Kann man Loops nutzen, um monatlich/quartalsweise
> abzufragen, ob es neue Klima-Maßnahmen gab?" — Ja, und so wird aus dem
> Adoptions-**Bug** ein **Feature**.

## Warum nicht `/loop`
Der `/loop`-Skill läuft *innerhalb einer Session* in kurzen Intervallen. Die
Remote-Container sind aber ephemer und werden nach Inaktivität recycelt — für
monatlich/quartalsweise ist das das falsche Werkzeug. Webhook-Events decken
„nichts ist passiert" ohnehin nicht ab.

## Das richtige Werkzeug: Scheduled Session (geplanter Trigger)
Claude Code on the web kann Sessions **zeitgesteuert** starten (cron-artig).
Doku: https://code.claude.com/docs/en/claude-code-on-the-web

| Feld | Wert |
|------|------|
| **Kadenz** | Quartalsende (z. B. `0 9 1 1,4,7,10 *`) — monatlich für `klima-alerts` denkbar |
| **Branch** | frische Session auf `main` |
| **Prompt** | „Führe `context-packs/refresh-sweep.pack.yaml` über `objects/` aus. Poste je Fund Objekt + Owner + Rückfrage nach `#klima-alerts` und als DM an den Owner. Erstelle KEINE Änderungen an Objekten — nur Anstöße." |
| **Netzwerk** | nur Slack-Zustellung nötig (Policy entsprechend) |

## Ablauf
1. Trigger feuert → frische Session startet.
2. Session lädt den Objektgraphen (`objects/`) + `refresh-sweep.pack.yaml`.
3. Führt die Sweep-Abfragen aus (überfällig, festhängende Ziele, vorläufige KPIs,
   Initiativen ohne neue Aktivität, offene Findings vor Reporting).
4. Stellt pro Fund eine **gezielte Rückfrage an den Owner** zu (Slack).
5. Owner antwortet dort, wo die Arbeit passiert — Pflege bleibt Teil der Arbeit
   (vgl. `../../MAINTAINING.md`: „Auslöser, nicht Kalender").

## Warum das das Risiko entschärft
Das Modell ist elegant, aber jemand muss die Objekte aktuell halten. Statt auf
Disziplin zu hoffen, macht der Trigger **Frische abfragbar und proaktiv**: Weil
jedes Objekt `stand`, `review_zyklus` und `owner` trägt, kann das System selbst
fragen *„Gab es seit Q1 neue Klima-Maßnahmen, die in `initiative-scope3-supplier-engagement`
fehlen?"* — adressiert an genau die Person, die es weiß.

> Einrichtung: Sag Bescheid, dann lege ich den Trigger (bzw. einen `/loop`-Fallback
> für kurze Intervalle) konkret an.
