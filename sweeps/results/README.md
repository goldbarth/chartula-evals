# Vergleichsergebnisse

Automatisch erzeugt durch `tools/sweep_results.py`; nicht von Hand bearbeiten.
Vorhandene Messwerte werden aufbereitet; Judging und Rubriken bleiben eingefroren.

## Vergleichsreihen

- [Oktober 2026: vier reale Szenarien](october/report.md): 84 Versuche, 74 vollständig, 12 Charts.
- [September 2026: Einstellungen an ServiceDeskLite](september/report.md): 43 Versuche, 42 vollständig, 16 Charts.
- [Änderung #338: vorher und nachher](change-338/report.md): 10 Versuche, 4 vollständig, 6 Charts.

## Reproduzieren

```bash
python3 tools/sweep_results.py --out sweeps/results --png
```

SVG, HTML, Markdown und CSV benötigen nur Python.
PNG benötigt zusätzlich `rsvg-convert`.
Die historische Preistabelle wird unverändert verwendet.
Berechnete Kosten nach Cache sind nicht gegen eine Rechnung verifiziert.
Alle Eingabedateien und ihre SHA-256-Prüfsummen stehen in `manifest.json`.
Exports enthalten keine Schlüsselkennungen, Rohtexte oder Meldungsbegründungen.
Repository- und PR-Metadaten vor öffentlicher Weitergabe prüfen.
