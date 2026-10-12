# Gespeicherte Vergleichsergebnisse auswerten

`tools/sweep_results.py` bereitet vorhandene Messwerte auf und erzeugt lokale Berichte mit statischen Charts.
Judging und Rubriken bleiben eingefroren.
Das Werkzeug erzeugt keine neuen Texte und ruft kein Modell auf.

```bash
python3 tools/sweep_results.py --out sweeps/results --png
python3 -m unittest discover -s tools -p 'test_sweep_results.py'
```

Ohne `--png` genügen Python und seine Standardbibliothek.
Für PNG-Exporte muss `rsvg-convert` installiert sein.
Öffne anschließend `sweeps/results/index.html` im Browser oder lies `sweeps/results/README.md`.
Ein bereits befüllter Ausgabeordner wird nur akzeptiert, wenn sein Manifest ihn als Ausgabe dieses Werkzeugs ausweist.

## Vergleichsreihen

- Oktober 2026: vier reale Szenarien, mit historischer Preistabelle vom 9. Oktober.
- September 2026: ServiceDeskLite mit Thinking-Stufen, unterschiedlichen Prüfern, Faktentiefen und lokalen Modellen; Preistabelle vom 25. September.
- Änderung #338: getrennte Vorher/Nachher-Reihe, mit unterschiedlichen Versionen und Prompt-Hashes.

Pläne ohne Ergebnisordner werden im Manifest genannt, nicht als Messungen ergänzt.
Die Reihen werden nicht zu einer Gesamtrangliste zusammengezogen.

## Bezugsgrößen

Ein vollständiger Lauf liefert alle angeforderten Zielgruppen und hat den Sweep-Status `ok`.
Die Abschlussquote zählt alle gespeicherten Versuche einschließlich fehlgeschlagener und nicht abgeschlossener Versuche.
Kosten- und Laufzeitmediane berücksichtigen nur vollständige Läufe.
Bekannte Messwerte unvollständiger Versuche werden als Kreuze gezeigt.

Kennzahlen je Zielgruppe berücksichtigen jedes vorhandene Rendering, auch aus einem teilweise vollständigen Lauf.
Fehlende Texte, Messwerte und Preise bleiben unbekannt; sie werden nicht zu null.
Die Zahl der Einträge zählt Listenzeilen mit `- ` und ist keine Faktenabdeckung.
Textlänge zählt Zeichen einschließlich Markdown im gespeicherten Rendering.

Die Phasenkosten verwenden Mittelwerte, damit Generierung und Prüfung addierbar bleiben.
Kosten ohne Cache dienen dem Konfigurationsvergleich.
Kosten nach Cache sind aus gespeicherten Tokens und historischen Preisen berechnet, nicht gegen Rechnungen verifiziert.
Die Kennzahl Ausgaben je vollständigem Lauf teilt die Kosten sämtlicher Versuche durch die Zahl vollständiger Läufe.
Sie bleibt bei unbekannten Kosten, Kostenuntergrenzen oder null vollständigen Läufen unbekannt.
Sie ist keine Prognose einer Wiederholungsstrategie.

Meldungen werden nicht als bestätigte Fehler interpretiert.
Wiederholung meint dieselbe PR in derselben Zielgruppe, nicht zwingend dieselbe Meldungsbegründung.
Die Prüfer sehen jeweils neu erzeugte Texte; ein isolierter Vergleich der Prüfer ist daraus nicht möglich.
Lokale Modelle haben null API-Kosten; Energie, Hardware und Betrieb sind nicht gemessen.

## Dateien und Herkunft

Jede Reihe enthält HTML und Markdown, SVG und optional PNG, sowie `runs.csv`, `configurations.csv`, `flag-overlap.csv` und `data-issues.csv`.
`manifest.json` hält die SHA-256-Prüfsummen der Eingaben und des Generators fest.
Die CSV-Exporte enthalten keine Schlüsselkennungen, Rohtexte oder Meldungsbegründungen.
Die Ergebnisse bleiben eine lokale Arbeitsfassung; Repository- und PR-Metadaten vor öffentlicher Weitergabe prüfen.

Rohdaten, bestehende Statistikexporte, Rubriken, Labels und Judge-Ergebnisse werden nicht geschrieben.
