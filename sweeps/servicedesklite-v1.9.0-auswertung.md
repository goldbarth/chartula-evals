# Auswertung: Vergleichsläufe ServiceDeskLite v1.9.0

Stand: 2026-09-25.
Fall: `goldbarth/ServiceDeskLite` `v1.9.0 --since 675555a7` (v1.7.0), 19 Commits, 18 Fakten, `--no-publish`.
Chartula: `0.1.0-preview.3+7620e6d` in allen 43 Versuchen.
14 Zellen mit je 3 gültigen Läufen, 1 gescheiterter Versuch (granite-Zelle).
Alle Zahlen aus den Run-Records, erzeugt mit `python3 tools/sweep_stats.py report sweeps/servicedesklite-v1.9.0 sweeps/prices-2026-09-25.json`.
Tabellen, Rohdaten und Grafiken: `sweeps/servicedesklite-v1.9.0-stats/` (`report.md`, `runs.csv`, `flags.csv`, `cells.csv`, `flags-by-pr.csv`, `axis-a.svg`, `axis-b.svg`).
Kosten: OpenAI-Listenpreis, Standard-Tarif, Stichtag 2026-09-25 (`sweeps/prices-2026-09-25.json`), ohne Cache, damit die Laufreihenfolge die Zahlen nicht verschiebt.
Jede Zahl ist der Median von 3 Läufen, in Klammern Min-Max.

## Was die Daten nicht tragen

- n = 3 pro Zelle. Unterschiede von einem Flag pro Lauf liegen in allen Zellen innerhalb der Spannweite; sie sind keine Aussage.
- Die Zahl der Flags sagt nicht, ob ein Flag berechtigt ist, und nichts über die Qualität der Texte. Die Texte wurden nicht mit der Rubric bewertet. Flag-Texte habe ich für Achse B und die lokalen Zellen gelesen, für Achse A nur #233.
- Ein Fall, ein Release, eine Repository-Art. Die Release-Größe ist nicht gemessen (aus Budgetgründen entschieden).
- terra ist nicht gemessen (entschieden: schwächer als sol, eine Generation älter, teurer im Output als gpt-6-sol).

## Achse A: Render-Modell und Thinking (Check: gpt-6-sol, disabled)

| Render | Thinking | Kosten $ | davon Rendern $ | Reasoning-Tokens | Dauer s | Flags/Lauf |
|---|---|---|---|---|---|---|
| gpt-6-luna | disabled | 0,0512 (0,0510-0,0512) | 0,0029 | 0 | 32 (30-35) | 4 (3-4) |
| gpt-6-luna | low | 0,0521 (0,0511-0,0530) | 0,0033 | 803 (644-926) | 43 (39-45) | 4 (3-5) |
| gpt-6-luna | medium | 0,0545 (0,0515-0,0549) | 0,0054 | 4.608 (3.074-6.103) | 72 (55-83) | 4 (2-6) |
| gpt-6-luna | high | 0,0552 (0,0550-0,0574) | 0,0075 | 8.879 (8.276-10.994) | 128 (124-137) | 3 (3-4) |
| gpt-6-sol | disabled | 0,1048 (0,1047-0,1055) | 0,0569 | 0 | 40 (39-40) | 3 (3-4) |
| gpt-6-sol | low | 0,1055 (0,1044-0,1066) | 0,0578 | 69 (63-76) | 48 (47-51) | 4 (2-5) |
| gpt-6-sol | medium | 0,1181 (0,1124-0,1286) | 0,0707 | 1.319 (581-2.167) | 76 (69-94) | 3 |
| gpt-6-sol | high | 0,1701 (0,1635-0,1859) | 0,1230 | 6.252 (5.510-7.680) | 170 (161-208) | 3 |

Der Check auf gpt-6-sol kostet in jeder Zelle 0,048 $ pro Lauf; bei luna ist er über 90 % der Kosten.

**Antwort.**
Thinking senkt die Flags in keiner Stufe: alle acht Zellen liegen bei 3 oder 4 Flags pro Lauf, die Spannweiten überlappen.
Thinking erhöht Dauer und Kosten: bei sol von `disabled` zu `high` die Kosten um 62 % (0,105 auf 0,170 $) und die Dauer um das 4,3-Fache (40 auf 170 s); bei luna die Dauer um das 4-Fache (32 auf 128 s) bei fast gleichen Kosten.
Das beste Verhältnis aus Kosten und Flags hat **gpt-6-luna mit `disabled`**: 0,051 $ mit Check, davon 0,003 $ fürs Rendern, 32 s, 4 (3-4) Flags, gegen sol `disabled` mit 0,105 $, 40 s, 3 (3-4) Flags.
Der Unterschied von einem Flag zwischen luna und sol trägt bei n = 3 nicht.
Nicht bestätigt: ob luna und sol gleich gute Texte schreiben. Das misst die Flag-Zahl nicht.

Der stabilste Flag hängt nicht am Modell, sondern am Fakt: #233 ist in 7 von 8 Zellen in 3 von 3 Läufen geflaggt (luna `medium`: 2 von 3).
Grund laut Flag-Text: #244 hat die Implementierung aus #233 wieder entfernt, #245 hat die Badges neu eingeführt; die Faktenbasis führt #233 trotzdem als eigene Änderung.

## Achse B: Render × Check (Thinking beide `disabled`)

| Render ↓ / geprüft von → | gpt-6-luna | gpt-6-sol |
|---|---|---|
| gpt-6-luna | **6**, technisch 0, Kunde 6 (Selbstprüfung) | 4 (3-4), technisch 1, Kunde 3 (2-3) |
| gpt-6-sol | 5 (4-8), technisch 0, Kunde 5 (4-8) | **3 (3-4)**, technisch 1 (1-2), Kunde 2 (Selbstprüfung) |

**Antwort.**
Die Flags hängen vom Prüfer ab, stärker als vom Renderer: luna als Prüfer meldet 6 bzw. 5 Flags pro Lauf, sol als Prüfer 4 bzw. 3.
luna als Prüfer flaggt nur die Kundensicht (0 technische Flags in 6 Läufen); sol flaggt in jedem seiner Läufe mindestens einen technischen Eintrag.
Ein Teil von lunas Mehr ist kein Befund: mindestens 7 der 35 luna-Flags sagen in der eigenen Begründung, die Stelle sei belegt ("The wording is supported.", "Supported by [#222]."). Bei sol als Prüfer: keiner von 88 Flags in allen sol-geprüften Zellen (per Textmuster gesucht, jeden Treffer gelesen).
Prüft ein Modell sich selbst milder? Die Daten zeigen das nicht: luna prüft sich selbst mit 6 Flags, sols Text mit 5; sol prüft sich selbst mit 3 (3-4), lunas Text mit 4 (3-4). Der eine Flag Unterschied bei sol liegt in derselben Spannweite.
Kosten: luna als Prüfer 0,0025 $ statt 0,048 $ pro Lauf.

## Nebenachsen (gegen `gpt-6-sol-disabled`: 0,1048 $, 40 s, 3 (3-4) Flags)

| Zelle | Input-Tokens | Kosten $ | Dauer s | Flags/Lauf |
|---|---|---|---|---|
| Referenz `gpt-6-sol-disabled` | 43.751 | 0,1048 | 40 | 3 (3-4), technisch 1 (1-2), Kunde 2 |
| thorough aus | 21.293 | 0,0572 | 34 | 0 |
| `factBase.depth: title-only` | 5.876 | 0,0230 | 29 | 1 (1-2), technisch 0, Kunde 1 (1-2) |

**thorough.**
Ohne den thorough-Check meldet kein Lauf einen Flag: die regelbasierte Prüfung fand in allen 42 Läufen des Sweeps nichts.
Mit thorough auf gpt-6-sol kommen 3 (3-4) Flags pro Lauf hinzu, für 0,048 $ (+83 % Kosten) und 6 s mehr pro Lauf.
Ob sich das lohnt, hängt daran, wie viele der Flags berechtigt sind; das ist hier nicht bewertet. Die Flag-Review vom 24.09. fand Fehlalarme (ROADMAP, "Geparkt aus der Flag-Review").
Belegt ist: ohne thorough bleibt z. B. #233 in diesem Fall unbemerkt, der in 3 von 3 Referenzläufen geflaggt wird und nach Flag-Text eine bereits entfernte Implementierung als Änderung beschreibt.

**factBase.depth.**
`title-only` senkt Input-Tokens um 87 % und Kosten um 78 %, die Flags von 3 auf 1.
Weniger Flags heißt hier weniger Stoff, nicht bessere Texte: ohne Beschreibung gibt es weniger, was der Text überdehnen kann. Was die Texte an Inhalt verlieren, ist nicht gemessen.

**Release-Größe.** Nicht gemessen.

## Lokal: qwen3:14b rendert (Ollama 0.33.3, RTX 4080 SUPER, `num_ctx 24576`)

| Zelle | Versuche | Dauer s | davon Check s | Flags/Lauf | notEvaluated |
|---|---|---|---|---|---|
| geprüft von qwen3 | 3 / 3 | 90 (71-97) | 32 | 17 (0-28) | 0 |
| geprüft von granite | 3 / 4 | 219 (48-677) | 164 | 3 (0-4) | 0 (im gescheiterten Versuch 1) |

Kosten 0 $ (Strom und Hardware nicht bewertet).

**qwen3:14b als Renderer: nein.**
In 7 Versuchen: einmal lehnte Chartula das Kunden-Rendering ab ("an entry for fact 18, which it was not sent"); einmal (`qwen3-14b-checked-by-qwen3-14b/run-2`) stand das Beispiel aus dem Prompt ("Saving over a network drive") als Eintrag in `release-v1.9.0.md`.
In keinem der 36 GPT-Läufe steht ein Prompt-Beispiel im Ergebnis (per Textsuche nach beiden Beispiel-Labels).

**qwen3:14b als Prüfer: nein.**
0, 28 und 17 Flags in drei Läufen; im Lauf mit 17 Flags sagen 13 in der Begründung "The facts support this claim".
Den erfundenen Netzlaufwerk-Eintrag hat er allerdings geflaggt (3 Flags).

**granite4.1-guardian:8b als Prüfer: nein.**
Das Antwortschema hält er formal ein (`notEvaluated` 0 in den gültigen Läufen), inhaltlich nicht: 2 von 7 Flags enthalten statt einer Begründung ein `<think>`-Protokoll.
Ein Check-Call scheiterte an einem `finish_reason`, den das SDK nicht kennt; ein anderer dauerte 618 s mit einer Wiederholung.
Ein Lauf endete mit 0 Flags nach 40 Output-Tokens.

## Entscheidungsvorlage: offene Launch-Punkte

Beobachtet am 25.09. mit dem installierten preview.3; entschieden ist nichts.

1. **`install.sh`-Abschlussmeldung nennt nur Anthropic: bestätigt.**
   Wortlaut: "Chartula needs two keys": `ANTHROPIC_API_KEY`, `GITHUB_TOKEN`. Für OpenAI braucht es Key, Provider, Base-URL und Modell.
2. **Schreibrecht des Tokens vor dem ersten Modellaufruf: heute nicht beobachtbar** (`--no-publish`).
   Im preview.3-Code keine Vorabprüfung gefunden (gesucht nach `permission`, `403` in `Cli/Commands`, `Core/Pipeline`); Beleg bleibt der Befund vom 23.09.
   Verwandt: der Token sah das private Repo nicht (HTTP 404); aufgefallen durch meinen Prüfbefehl, nicht durch Chartula. Wie Chartula das meldet, ist nicht getestet.
3. **Doku "Anderen Provider nutzen": gebraucht.**
   Heute nötig und nirgends als Rezept: `Chartula__Llm__Provider=openai-compatible`, `Chartula__Llm__BaseUrl=https://api.openai.com/v1` (kein Default), `OPENAI_API_KEY`, gültige Modell-ID (`gpt-6-terra` gibt es nicht), für Ollama `num_ctx`.
   Die fehlende Base-URL fiel im Sweep-Plan erst durch deine Rückfrage auf.
   Ein Tippfehler im Variablennamen (`OPEN_API_KEY`) blieb unbemerkt, weil ein anderer gültiger Key gesetzt war; Chartula kann das nicht erkennen.
4. **`chartula init` / `chartula doctor`: hätte heute Schritte erspart.**
   Von Hand geprüft: installierte Version (kein `--version`), Base-URL, Modell-ID, Lesezugriff des Tokens aufs Repo, Ollama-Modell vorhanden, Ollama-Kontextfenster.
   Jeder dieser Punkte wäre sonst erst im Lauf aufgefallen; ob Chartulas Meldung dann Ursache und Fix nennt, ist nicht geprüft.
5. **Kleine Issues:** die #210-Klasse ist heute erneut aufgetreten: die Kopfzeile sagt "key from OPENAI_API_KEY", obwohl die Variable nicht gesetzt war.
