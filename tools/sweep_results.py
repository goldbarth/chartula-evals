#!/usr/bin/env python3
"""Build local measurement reports from saved sweeps, without model or network calls.

    python3 tools/sweep_results.py --out sweeps/results
    python3 tools/sweep_results.py --out sweeps/results --png

SVG charts and HTML/Markdown reports use only the Python standard library.
PNG export additionally requires rsvg-convert.
Existing statistics, raw run material, rubrics and judge results are never written.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import math
import shutil
import statistics
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

from sweep_stats import price

AUDIENCES = ('technical', 'customer')
CASE_ORDER = ('small', 'typical', 'large', 'difficult')
CASE_NAMES = {'small': 'Klein', 'typical': 'Typisch', 'large': 'Groß', 'difficult': 'Schwierige Quelldaten'}
COLORS = {'openai': '#2563a6', 'anthropic': '#087e73', 'local': '#7552a0', 'unknown': '#626d7b'}
INK, MUTED, GRID, ORANGE = '#172b42', '#52677c', '#dce4ec', '#b66615'
FIELDS = ['runId', 'case', 'configuration', 'label', 'provider', 'run', 'status', 'complete',
          'hasRecord', 'model', 'thinking', 'checkModel', 'checkThinking', 'thoroughCheck',
          'factBaseDepth', 'toolVersion', 'promptHash', 'factsSha256', 'rangeFromCommit', 'rangeToCommit',
          'facts', 'pullRequests', 'factsWithDescription', 'descriptionCharacters',
          'billedUsd', 'uncachedUsd', 'renderUncachedUsd', 'checkUncachedUsd', 'costIsLowerBound',
          'durationSeconds', 'renderSeconds', 'checkSeconds', 'inputTokens', 'outputTokens',
          'reasoningTokens', 'cachedInputTokens', 'callsWithoutUsage', 'retries', 'notEvaluated',
          'technicalRendered', 'technicalCharacters', 'technicalEntries', 'technicalFlags',
          'customerRendered', 'customerCharacters', 'customerEntries', 'customerFlags']


def esc(value):
    return html.escape(str(value), quote=True)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def median(values):
    found = [v for v in values if v is not None]
    return statistics.median(found) if found else None


def fmt(value, digits=2):
    if value is None:
        return 'unbekannt'
    return f'{value:,.{digits}f}'.replace(',', '_').replace('.', ',').replace('_', '.')


def compact(value):
    if value >= 1000:
        return fmt(value / 1000, 1) + 'k'
    return fmt(value, 3 if 0 < value < .1 else 2 if value < 1 else 0)


def write_csv(path, rows, fields):
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


def label_for(cell, record, meta, stage):
    if stage:
        return 'Vorher · Sonnet 5' if stage == 'before' else 'Nachher · Sonnet 5'
    if meta:
        provider = 'OpenAI' if meta['provider'] == 'openai' else 'Anthropic'
        return f"{provider} {meta['configuration'].upper()}"
    label = cell.replace('gpt-6-', '').replace('checked-by-', 'Prüfer ').replace('-disabled', ' · aus').replace('-no-thorough', ' · ohne Prüfung').replace('-title-only', ' · nur Titel').replace('qwen3-14b', 'Qwen 14B').replace('granite4.1-guardian-8b', 'Granite 8B')
    for suffix, text in [('low', 'niedrig'), ('medium', 'mittel'), ('high', 'hoch')]:
        label = label.replace('-' + suffix, ' · ' + text)
    return label



def collect(repo, jobs, prices, inputs, issues):
    rows, flags = [], []
    for plan_path, case, stage in jobs:
        inputs.add(plan_path)
        plan = json.loads(plan_path.read_text())
        folder = repo / 'sweeps' / plan_path.stem
        expected = ['customer'] if stage else list(AUDIENCES)
        meta_cells = {c['name']: c for c in plan['cells'] if 'provider' in c}
        for cell in sorted(folder.iterdir()):
            if not cell.is_dir() or cell.name.startswith('_'):
                continue
            for run in sorted(cell.glob('run-*')):
                if not run.is_dir():
                    continue
                marker = run / 'sweep-run.json'
                result = json.loads(marker.read_text()) if marker.exists() else {}
                if marker.exists():
                    inputs.add(marker)
                records = sorted(run.glob('run-record-*.json'))
                status = result.get('status', 'failed' if '.failed-' in run.name else 'running')
                configuration = f'{stage}-{cell.name}' if stage else cell.name
                row = dict.fromkeys(FIELDS)
                row.update(runId=str(run.relative_to(repo)), case=case, configuration=configuration,
                           run=run.name, status=status, complete=False, hasRecord=bool(records))
                meta = meta_cells.get(cell.name)
                if meta:
                    row['provider'] = meta['provider']
                if not records:
                    row['label'] = label_for(cell.name, {}, meta, stage)
                    issues.append({'runId': row['runId'], 'kind': 'missing_record',
                                   'detail': 'Kein Run-Record; Kosten, Dauer und Zielgruppenergebnisse unbekannt.'})
                    rows.append(row)
                    continue
                if len(records) != 1:
                    raise ValueError(f'{run}: expected one run record, found {len(records)}')
                inputs.add(records[0])
                record = json.loads(records[0].read_text())
                prov, metrics = record['provenance'], record['metrics']
                render, check = metrics['rephrase'], metrics['faithfulnessCheck']
                row.update({k: prov.get(k) for k in ['model', 'thinking', 'checkModel', 'checkThinking',
                                                    'thoroughCheck', 'factBaseDepth', 'toolVersion', 'promptHash']})
                row['provider'] = row['provider'] or ('local' if ':' in prov['model'] else 'anthropic' if prov['model'].startswith('claude') else 'openai')
                row['label'] = label_for(cell.name, record, meta, stage)
                row.update({k: metrics['release'].get(k) for k in ['facts', 'pullRequests', 'factsWithDescription', 'descriptionCharacters']})
                for key, source in [('durationSeconds', metrics), ('renderSeconds', render), ('checkSeconds', check)]:
                    row[key] = source.get('durationSeconds')
                for key in ['inputTokens', 'outputTokens', 'retries', 'cachedInputTokens', 'callsWithoutUsage']:
                    row[key] = render.get(key, 0) + check.get(key, 0)
                reasoning = [render.get('reasoningTokens'), check.get('reasoningTokens')]
                row['reasoningTokens'] = sum(reasoning) if all(v is not None for v in reasoning) else None
                row['costIsLowerBound'] = row['callsWithoutUsage'] > 0
                row['notEvaluated'] = metrics.get('thoroughCheck', {}).get('notEvaluated')
                if prov['model'] in prices and (not prov.get('thoroughCheck') or prov.get('checkModel') in prices):
                    rb, ru = price(prices, prov['model'], render)
                    cb, cu = price(prices, prov['checkModel'], check) if prov.get('thoroughCheck') else (0, 0)
                    row.update(billedUsd=rb + cb, uncachedUsd=ru + cu, renderUncachedUsd=ru, checkUncachedUsd=cu)
                else:
                    issues.append({'runId': row['runId'], 'kind': 'unknown_price', 'detail': 'Keine passende historische Preistabelle; Kosten bleiben unbekannt.'})
                if record.get('facts') is not None:
                    row['factsSha256'] = hashlib.sha256(json.dumps(record['facts'], sort_keys=True, ensure_ascii=False).encode()).hexdigest()
                for key in ['rangeFromCommit', 'rangeToCommit']:
                    row[key] = record.get('range', {}).get('fromCommit' if key == 'rangeFromCommit' else 'toCommit')
                changelog = run / 'changelog.json'
                texts = {}
                if changelog.exists():
                    inputs.add(changelog)
                    texts = json.loads(changelog.read_text()).get('renderings', {})
                audiences = {a['audience']: a for a in record['audiences']}
                row['complete'] = status == 'ok' and all(audiences.get(a, {}).get('rendered') is True for a in expected)
                if status == 'ok' and not row['complete']:
                    issues.append({'runId': row['runId'], 'kind': 'status_conflict', 'detail': 'Status ok, aber angeforderte Zielgruppe fehlt.'})
                for audience in AUDIENCES:
                    data = audiences.get(audience)
                    row[audience + 'Rendered'] = data.get('rendered') if data else None
                    text = texts.get(audience)
                    if data and data.get('rendered') and text is None:
                        issues.append({'runId': row['runId'], 'kind': 'missing_text', 'detail': f'{audience}: gerendert, aber gespeicherter Text fehlt.'})
                    if text is not None and data and data.get('rendered'):
                        row[audience + 'Characters'] = len(text)
                        row[audience + 'Entries'] = sum(line.startswith('- ') for line in text.splitlines())
                    if data and data.get('rendered') and 'flags' in data:
                        row[audience + 'Flags'] = len(data['flags'])
                        for f in data['flags']:
                            flags.append({'runId': row['runId'], 'case': case, 'configuration': configuration,
                                          'audience': audience, 'pullRequest': f.get('pullRequest')})
                if meta:
                    for field, envkey in [('model', 'Chartula__Llm__Model'), ('thinking', 'Chartula__Llm__Thinking'),
                                          ('checkModel', 'Chartula__Faithfulness__Model'), ('checkThinking', 'Chartula__Faithfulness__Thinking')]:
                        if row[field] != meta['env'].get(envkey):
                            raise ValueError(f'{row["runId"]}: {field} differs from plan')
                rows.append(row)
    return rows, flags


def groups(rows):
    result = defaultdict(list)
    for r in rows:
        result[(r['case'], r['configuration'])].append(r)
    return result


def ordered_configs(rows):
    configs = {r['configuration'] for r in rows}
    tier = {'g-g': 0, 'g-m': 1, 'm-m': 2, 'p-m': 3}
    def key(c):
        if c.startswith(('before-', 'after-')):
            return (0, 0 if c.startswith('before-') else 1, c)
        r = next(r for r in rows if r['configuration'] == c and r['hasRecord'])
        parts = c.split('--')[0].split('-', 1)
        if len(parts) == 2 and parts[1] in tier:
            return (0 if parts[0] == 'openai' else 1, tier[parts[1]], c)
        return (2, 0, c)
    return sorted(configs, key=key)


class SVG:
    def __init__(self, width, height, title, subtitle):
        self.width, self.height = width, height
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
                      f'<title id="title">{esc(title)}</title><desc id="desc">{esc(subtitle)}</desc>',
                      '<style>text{font-family:DejaVu Sans,Arial,sans-serif}text{fill:#172b42}</style>',
                      f'<rect width="{width}" height="{height}" fill="#fff"/>']
        self.text(30, 35, title, 22, weight='700')
        self.text(30, 62, subtitle, 12, color=MUTED)

    def text(self, x, y, value, size=12, color=INK, anchor='start', weight='400'):
        size += 1 if size < 17 else 0
        self.parts.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" style="fill:{color}" text-anchor="{anchor}" font-weight="{weight}">{esc(value)}</text>')

    def line(self, x1, y1, x2, y2, color=GRID, width=1):
        self.parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{width}"/>')

    def rect(self, x, y, w, h, color, tip=None):
        self.parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="3" fill="{color}">{"<title>" + esc(tip) + "</title>" if tip else ""}</rect>')

    def dot(self, x, y, color, tip, partial=False, radius=4):
        self.parts.append(f'<g><title>{esc(tip)}</title>')
        if partial:
            self.line(x - radius, y - radius, x + radius, y + radius, ORANGE, 2)
            self.line(x - radius, y + radius, x + radius, y - radius, ORANGE, 2)
        else:
            self.parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" fill="{color}"/>')
        self.parts.append('</g>')

    def save(self, path):
        path.write_text('\n'.join(self.parts) + '\n</svg>\n', encoding='utf-8')


def layout(rows):
    cases = [c for c in CASE_ORDER if any(r['case'] == c for r in rows)]
    configs = ordered_configs(rows)
    cols = 2 if len(cases) > 1 else 1
    pw = 850 if cols == 2 else 1300
    ph = 142 + 34 * len(configs)
    return cases, configs, cols, pw, ph


def chart_completion(rows, path):
    cases, configs, cols, pw, ph = layout(rows)
    svg = SVG(pw * cols, 105 + math.ceil(len(cases) / cols) * ph,
              'Welche Läufe liefern vollständig?',
              'Blaugrün: vollständig · Orange: teilweise · Rot: fehlgeschlagen · Grau: Status unbekannt / laufend; Details in runs.csv')
    by = groups(rows)
    for i, case in enumerate(cases):
        x, y = (i % cols) * pw + 30, 100 + (i // cols) * ph
        svg.text(x, y, CASE_NAMES[case], 17, weight='700')
        svg.text(x + 380, y, 'Einzelversuche', 11, color=MUTED)
        svg.text(x + 590, y, 'vollständig / Versuche', 11, color=MUTED)
        for j, config in enumerate(configs):
            yy = y + 34 * (j + 1)
            mine = by.get((case, config), [])
            label = next(r['label'] for r in rows if r['configuration'] == config)
            svg.text(x, yy + 4, label, 12)
            if not mine:
                svg.text(x + 390, yy + 4, 'nicht gemessen', color=MUTED)
                continue
            for k, r in enumerate(mine):
                color = '#087e73' if r['complete'] else '#bb6d1c' if r['status'] == 'incomplete' else '#b6404d' if r['status'] == 'failed' else '#8d99a5'
                svg.rect(x + 380 + k * 23, yy - 9, 17, 17, color, f"{r['run']}: {r['status']}; technical={r['technicalRendered']}, customer={r['customerRendered']}")
            svg.text(x + 600, yy + 4, f"{sum(r['complete'] for r in mine)} / {len(mine)}", 13, weight='700')
        svg.text(x, y + ph - 20, 'Vollständig heißt: alle angeforderten Zielgruppen gerendert; keine Qualitätsaussage.', 11, color=MUTED)
    svg.save(path)


def chart_metric(rows, path, key, title, unit, audience=None):
    cases, configs, cols, pw, ph = layout(rows)
    values = [r[key] for r in rows if r[key] is not None and (not audience or r[audience + 'Rendered'])]
    if not values:
        return False
    top = max(values) * 1.08 or 1
    svg = SVG(pw * cols, 105 + math.ceil(len(cases) / cols) * ph, title,
              f'{unit} · Punkte: einzelne Läufe · schwarzer Strich: Median · Linie: beobachtetes Min–Max · X: unvollständiger Versuch')
    by = groups(rows)
    label_width = 360 if cols == 1 else 265
    plot_width = pw - label_width - 235
    for i, case in enumerate(cases):
        x, y = (i % cols) * pw + 30, 100 + (i // cols) * ph
        svg.text(x, y, CASE_NAMES[case], 17, weight='700')
        for t in range(5):
            xx = x + label_width + plot_width * t / 4
            svg.line(xx, y + 20, xx, y + 34 * len(configs) + 14)
            svg.text(xx, y + ph - 35, compact(top * t / 4), 10, anchor='middle', color=MUTED)
        for j, config in enumerate(configs):
            yy = y + 34 * (j + 1)
            mine = by.get((case, config), [])
            label = next(r['label'] for r in rows if r['configuration'] == config)
            svg.text(x, yy + 4, label, 11)
            if not mine:
                svg.text(x + label_width, yy + 4, 'nicht gemessen', color=MUTED)
                continue
            eligible = [r for r in mine if r[key] is not None and (not audience or r[audience + 'Rendered'])]
            full = eligible if audience else [r for r in eligible if r['complete']]
            xs = lambda v: x + label_width + v / top * plot_width
            vals = [r[key] for r in full]
            if vals:
                svg.line(xs(min(vals)), yy, xs(max(vals)), yy, '#8396a8', 2)
                svg.line(xs(median(vals)), yy - 9, xs(median(vals)), yy + 9, INK, 2)
            for k, r in enumerate(eligible):
                svg.dot(xs(r[key]), yy + (k - (len(eligible) - 1) / 2) * 5,
                        COLORS.get(r['provider'], '#626d7b'), f"{r['run']}: {fmt(r[key], 4)} {unit}; {r['status']}", partial=not r['complete'])
            if vals:
                svg.text(x + label_width + plot_width + 18, yy + 4,
                         f"{fmt(median(vals), 4 if 'Usd' in key else 0)} · n={len(vals)}", 11)
            else:
                svg.text(x + label_width + plot_width + 18, yy + 4, 'Zielgruppe fehlt / Wert unbekannt' if audience else 'kein vollständiger Wert', 10, color=MUTED)
        note = 'Median über gerenderte Zielgruppen, auch aus teilweise vollständigen Läufen.' if audience else 'Median nur vollständig; unvollständige Versuche als X, keine Konfidenzintervalle.'
        svg.text(x, y + ph - 12, note, 10, color=MUTED)
    svg.save(path)
    return True


def chart_phases(rows, path):
    cases, configs, cols, pw, ph = layout(rows)
    by = groups(rows)
    means = {}
    for k, mine in by.items():
        full = [r for r in mine if r['complete'] and r['uncachedUsd'] is not None]
        if full:
            means[k] = (statistics.mean(r['renderUncachedUsd'] for r in full), statistics.mean(r['checkUncachedUsd'] for r in full), len(full))
    if not means:
        return False
    top = max(a + b for a, b, _ in means.values()) * 1.05 or 1
    svg = SVG(pw * cols, 105 + math.ceil(len(cases) / cols) * ph, 'Wo entstehen die API-Kosten?',
              'USD ohne Cache · Blau: Generierung · Orange: Prüfung · Mittelwerte vollständiger Läufe, damit die Teile addierbar sind')
    for i, case in enumerate(cases):
        x, y = (i % cols) * pw + 30, 100 + (i // cols) * ph
        svg.text(x, y, CASE_NAMES[case], 17, weight='700')
        label_width, plot_width = (360, 550) if cols == 1 else (265, 350)
        for j, config in enumerate(configs):
            yy = y + 34 * (j + 1)
            svg.text(x, yy + 4, next(r['label'] for r in rows if r['configuration'] == config), 11)
            values = means.get((case, config))
            if not values:
                svg.text(x + label_width, yy + 4, 'nicht gemessen / kein vollständiger Kostenwert', 10, color=MUTED)
                continue
            a, b, n = values
            svg.rect(x + label_width, yy - 9, a / top * plot_width, 18, '#2563a6')
            svg.rect(x + label_width + a / top * plot_width, yy - 9, b / top * plot_width, 18, '#bb6d1c')
            svg.text(x + label_width + plot_width + 12, yy + 4, f"{fmt(a + b, 4)} · Prüfung {fmt(100 * b / (a + b), 0) if a + b else '0'}%", 10)
        svg.text(x, y + ph - 20, 'Gemeinsame Skala; Summen und Phasenmittelwerte stehen in configurations.csv.', 10, color=MUTED)
    svg.save(path)
    return True


def chart_tradeoff(rows, path):
    full = [r for r in rows if r['complete'] and r['uncachedUsd'] is not None and r['durationSeconds'] is not None]
    if not full:
        return False
    cases, configs, cols, _, _ = layout(rows)
    single = len(cases) == 1
    pw = 1450 if single else 750
    ph = max(420, 90 + len(configs) * 29)
    width, height = pw * (1 if single else 2), 120 + math.ceil(len(cases) / 2) * ph
    plot_width = 820 if single else 440
    legend_x = plot_width + 35
    hi_x = max(r['uncachedUsd'] for r in full) * 1.12 or 1
    hi_y = max(r['durationSeconds'] for r in full) * 1.12 or 1
    svg = SVG(width, height, 'Kosten und Wartezeit gemeinsam betrachten',
              'USD ohne Cache gegen Gesamtdauer · Punkte: einzelne vollständige Läufe · Zahlen: Konfigurationen · keine Qualitätsrangliste')
    by = groups(rows)
    for i, case in enumerate(cases):
        x, y = i % 2 * pw + 65, 100 + i // 2 * ph
        svg.text(x - 35, y, CASE_NAMES[case], 17, weight='700')
        for t in range(5):
            xx, yy = x + plot_width * t / 4, y + 280 - 250 * t / 4
            svg.line(xx, y + 30, xx, y + 280)
            svg.line(x, yy, x + plot_width, yy)
            svg.text(xx, y + 300, compact(hi_x * t / 4), 10, anchor='middle', color=MUTED)
            svg.text(x - 8, yy + 3, compact(hi_y * t / 4), 10, anchor='end', color=MUTED)
        svg.text(x + plot_width / 2, y + 325, 'USD ohne Cache', 11, anchor='middle')
        svg.text(x - 35, y + 18, 'Sekunden', 10, color=MUTED)
        for j, config in enumerate(configs):
            mine = by.get((case, config), [])
            valid = [r for r in mine if r['complete'] and r['uncachedUsd'] is not None]
            for r in valid:
                svg.dot(x + r['uncachedUsd'] / hi_x * plot_width, y + 280 - r['durationSeconds'] / hi_y * 250,
                        COLORS[r['provider']], f"{r['label']} {r['run']}: {fmt(r['uncachedUsd'], 4)} USD, {fmt(r['durationSeconds'], 1)} s")
            if valid:
                xx = x + median([r['uncachedUsd'] for r in valid]) / hi_x * plot_width
                yy = y + 280 - median([r['durationSeconds'] for r in valid]) / hi_y * 250
                svg.text(xx + 8, yy - 8, j + 1, 11, weight='700')
            label = next(r['label'] for r in rows if r['configuration'] == config)
            svg.text(x + legend_x, y + 34 + j * 29, f"{j + 1}. {label}", 10)
            svg.text(x + legend_x + 10, y + 47 + j * 29, f"{sum(r['complete'] for r in mine)}/{len(mine)} vollständig" if mine else 'nicht gemessen', 9, color=MUTED)
    svg.save(path)
    return True


def chart_thinking(rows, path):
    selected = [r for r in rows if r['checkModel'] == 'gpt-6-sol' and r['checkThinking'] == 'disabled'
                and r['thoroughCheck'] and r['factBaseDepth'] == 'title-and-description' and r['complete']]
    models = ['gpt-6-luna', 'gpt-6-sol']
    levels = ['disabled', 'low', 'medium', 'high']
    panels = [('uncachedUsd', 'API-Kosten ohne Cache · USD'), ('durationSeconds', 'Gesamtdauer · Sekunden'),
              ('reasoningTokens', 'Reasoning-Tokens · gemeldete Summe')]
    svg = SVG(1440, 690, 'Was verändert die Thinking-Stufe?',
              'ServiceDeskLite, dieselbe Version und derselbe Prüfer · Einzelwerte, Median und beobachtetes Min–Max · keine Qualitätsmessung')
    for i, model in enumerate(models):
        for j, (metric, title) in enumerate(panels):
            x, y = 70 + j * 480, 110 + i * 280
            mine = [r for r in selected if r['model'] == model]
            vals = [r[metric] for r in selected if r[metric] is not None]
            hi = max(vals, default=1) * 1.1 or 1
            svg.text(x - 30, y, model + ' · ' + title, 13, weight='700')
            for t in range(5):
                yy = y + 195 - 165 * t / 4
                svg.line(x, yy, x + 340, yy)
                svg.text(x - 8, yy + 4, compact(hi * t / 4), 10, anchor='end', color=MUTED)
            for k, level in enumerate(levels):
                values = [r[metric] for r in mine if r['thinking'] == level and r[metric] is not None]
                xx = x + 40 + k * 85
                ys = lambda v: y + 195 - v / hi * 165
                svg.text(xx, y + 218, ['aus', 'niedrig', 'mittel', 'hoch'][k], 11, anchor='middle')
                if not values:
                    continue
                svg.line(xx, ys(min(values)), xx, ys(max(values)), '#8396a8', 2)
                svg.line(xx - 10, ys(median(values)), xx + 10, ys(median(values)), INK, 2)
                for n, v in enumerate(values):
                    svg.dot(xx + (n - 1) * 5, ys(v), '#2563a6', f'{model} {level}: {fmt(v, 4)}; n={len(values)}')
    svg.text(30, 665, 'Prüfer: gpt-6-sol, Thinking aus; gleiche Skala je Messgröße über beide Modelle. Reasoning-Tokens sind bereits in Ausgabetokens enthalten.', 11, color=MUTED)
    svg.save(path)


def flag_overlap(rows, flags):
    seen = defaultdict(set)
    for f in flags:
        if f['pullRequest'] is not None:
            seen[(f['case'], f['configuration'], f['audience'], f['pullRequest'])].add(f['runId'])
    by = groups(rows)
    return [dict(case=c, configuration=k, audience=a, pullRequest=p, flaggedRuns=len(ids),
                 renderedRuns=sum(r[a + 'Rendered'] is True for r in by[(c, k)]))
            for (c, k, a, p), ids in sorted(seen.items(), key=lambda item: str(item[0]))]


def chart_overlap(rows, overlap, path, audience):
    cases, configs, cols, pw, ph = layout(rows)
    svg = SVG(pw * cols, 105 + math.ceil(len(cases) / cols) * ph,
              f'Welche PRs erhalten wiederholt Meldungen? · {audience}',
              'PR-Zielgruppen-Paare, keine identischen Fehlertypen · dunkel: in allen gerenderten Wiederholungen · hell: in einem Teil')
    by = groups(rows)
    counts = Counter((o['case'], o['configuration']) for o in overlap if o['audience'] == audience)
    overlap_top = max(counts.values(), default=1)
    for i, case in enumerate(cases):
        x, y = i % cols * pw + 30, 100 + i // cols * ph
        svg.text(x, y, CASE_NAMES[case], 17, weight='700')
        for j, config in enumerate(configs):
            yy = y + 34 * (j + 1)
            svg.text(x, yy + 4, next(r['label'] for r in rows if r['configuration'] == config), 11)
            mine = by.get((case, config), [])
            n = sum(r[audience + 'Rendered'] is True for r in mine)
            if not n:
                svg.text(x + 300, yy + 4, 'nicht gemessen / Zielgruppe fehlt', 10, color=MUTED)
                continue
            keys = [o for o in overlap if o['case'] == case and o['configuration'] == config and o['audience'] == audience]
            persistent = sum(o['flaggedRuns'] == n for o in keys)
            varying = len(keys) - persistent
            svg.rect(x + 300, yy - 9, persistent / overlap_top * 285, 18, '#385f84')
            svg.rect(x + 300 + persistent / overlap_top * 285, yy - 9, varying / overlap_top * 285, 18, '#b7cce0')
            svg.text(x + 610, yy + 4, f'{persistent} ständig / {varying} wechselnd · n={n}', 10)
        svg.text(x, y + ph - 20, 'Bei n=1 heißt ständig nur: in der einzigen vorhandenen Wiederholung.', 10, color=MUTED)
    svg.save(path)


def summarize(rows):
    result = []
    for (case, config), mine in groups(rows).items():
        full = [r for r in mine if r['complete']]
        total_known = all(r['billedUsd'] is not None and not r['costIsLowerBound'] for r in mine)
        billed = sum(r['billedUsd'] for r in mine) if total_known else None
        known_costs = [r['billedUsd'] for r in mine if r['billedUsd'] is not None]
        known_spend = sum(known_costs) if known_costs else None
        cell = dict(case=case, configuration=config, label=mine[0]['label'], attempts=len(mine), complete=len(full),
                    incomplete=sum(r['status'] == 'incomplete' for r in mine), failed=sum(r['status'] == 'failed' for r in mine),
                    withoutRecord=sum(not r['hasRecord'] for r in mine), billedAllAttemptsUsd=billed,
                    knownBilledSubtotalUsd=known_spend, knownCostAttempts=len(known_costs),
                    lowerBoundAttempts=sum(r['costIsLowerBound'] is True for r in mine),
                    billedSpendPerCompleteUsd=billed / len(full) if billed is not None and full else None)
        for key in ['uncachedUsd', 'billedUsd', 'durationSeconds', 'renderSeconds', 'checkSeconds', 'inputTokens', 'outputTokens', 'reasoningTokens']:
            values = [r[key] for r in full if r[key] is not None]
            for suffix, value in [('Median', median(values)), ('Min', min(values) if values else None), ('Max', max(values) if values else None)]:
                cell[key + suffix] = value
        priced = [r for r in full if r['uncachedUsd'] is not None]
        for key in ['renderUncachedUsd', 'checkUncachedUsd']:
            cell[key + 'Mean'] = statistics.mean(r[key] for r in priced) if priced else None
        for a in AUDIENCES:
            available = [r for r in mine if r[a + 'Rendered'] is True]
            cell[a + 'RenderedRuns'] = len(available)
            for measure in ['Characters', 'Entries', 'Flags']:
                cell[a + measure + 'Median'] = median([r[a + measure] for r in available])
        result.append(cell)
    return result


def provenance_issues(rows, october, issues):
    if not october:
        return
    valid = [r for r in rows if r['hasRecord']]
    for key in ['toolVersion', 'promptHash', 'factBaseDepth', 'thoroughCheck']:
        if len({r[key] for r in valid}) != 1:
            raise ValueError(f'October comparison has inconsistent {key}')
    for case in CASE_ORDER:
        mine = [r for r in valid if r['case'] == case]
        for key in ['factsSha256', 'rangeFromCommit', 'rangeToCommit', 'facts']:
            if len({r[key] for r in mine}) != 1 or any(r[key] is None for r in mine):
                raise ValueError(f'{case}: inconsistent or absent {key}')


def html_table(headers, values):
    return '<div class="table-wrap"><table><thead><tr>' + ''.join(f'<th>{esc(h)}</th>' for h in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{esc(v)}</td>' for v in row) + '</tr>' for row in values) + '</tbody></table></div>'


CSS = '''body{margin:0;background:#f1f5f8;color:#172b42;font:16px/1.6 system-ui,sans-serif}main{max-width:1320px;margin:auto;padding:40px 28px}h1{font-size:clamp(28px,4vw,46px);line-height:1.2}h2{margin-top:42px}a{color:#1b5c98}.eyebrow{color:#52677c;font-size:13px;letter-spacing:.12em;text-transform:uppercase}.intro{max-width:850px;font-size:18px}.cards{display:flex;gap:16px;flex-wrap:wrap}.card{background:white;border:1px solid #dce4ec;border-radius:10px;padding:18px 24px;flex:1;min-width:180px}.number{font-size:32px;font-weight:700}.note{background:#fff8eb;border-left:4px solid #bb6d1c;padding:14px 20px}figure{margin:24px 0;background:white;padding:18px;border:1px solid #dce4ec;border-radius:10px}figure img{display:block;width:100%;height:auto}figcaption{font-size:14px;color:#52677c;margin-top:12px}.table-wrap{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;padding:9px 12px;border-bottom:1px solid #dce4ec}th{background:#e8eff5}.downloads{display:flex;gap:16px;flex-wrap:wrap}.small{font-size:14px;color:#52677c}code{background:#e5ecf2;padding:2px 5px}li{margin:6px 0}'''


def page(title, body):
    return f'<!doctype html>\n<html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)}</title><style>{CSS}</style><main>{body}</main></html>\n'


def build_series(repo, out, name, title, jobs, price_path, inputs, png):
    issues = []
    prices = {}
    if price_path:
        inputs.add(price_path)
        prices = json.loads(price_path.read_text())['models']
    rows, flags = collect(repo, jobs, prices, inputs, issues)
    if not rows:
        return None
    provenance_issues(rows, name == 'october', issues)
    folder = out / name
    folder.mkdir(parents=True, exist_ok=True)
    write_csv(folder / 'runs.csv', rows, FIELDS)
    cells = summarize(rows)
    write_csv(folder / 'configurations.csv', cells, list(cells[0]))
    overlap = flag_overlap(rows, flags)
    write_csv(folder / 'flag-overlap.csv', overlap, ['case', 'configuration', 'audience', 'pullRequest', 'flaggedRuns', 'renderedRuns'])
    write_csv(folder / 'data-issues.csv', issues, ['runId', 'kind', 'detail'])
    charts = []
    def add(filename, heading, description, func, *args):
        target = folder / (filename + '.svg')
        generated = func(rows, target, *args)
        if generated is False:
            return
        if png:
            subprocess.run(['rsvg-convert', str(target), '-o', str(target.with_suffix('.png'))], check=True)
        charts.append((filename, heading, description))
    add('completion', '1. Vollständigkeit', 'Jedes Quadrat steht für einen Versuch; auch Fehlversuche und fehlende Records bleiben sichtbar.', chart_completion)
    add('cost', '2. API-Kosten', 'Historische Listenpreise ohne Cache; der Median bezieht sich auf vollständige Läufe. Orange Kreuze zeigen bekannte Ausgaben unvollständiger Versuche.', chart_metric, 'uncachedUsd', 'Was kostet ein vollständiger Lauf?', 'USD ohne Cache')
    add('duration', '3. Wartezeit', 'Gesamtdauer inklusive Arbeit außerhalb der Modellphasen. Fehlende Dauer wird nicht als null ersetzt.', chart_metric, 'durationSeconds', 'Wie lange dauert ein Lauf?', 'Sekunden')
    add('cost-phases', '4. Kosten von Generierung und Prüfung', 'Arithmetische Mittelwerte vollständiger Läufe; die Phasen sind deshalb addierbar. Nicht die Summe unabhängiger Phasenmediane.', chart_phases)
    if name == 'september':
        add('thinking', 'Thinking-Stufen im direkten Vergleich', 'Nur die acht Konfigurationen mit festem gpt-6-sol-Prüfer, gleicher Faktentiefe und aktivem Thorough Check. Drei Wiederholungen je Stufe.', chart_thinking)
        settings = [r for r in rows if r['configuration'] in ['gpt-6-sol-disabled', 'gpt-6-sol-disabled-no-thorough', 'gpt-6-sol-disabled-title-only']]
        for filename, metric, heading, unit in [('settings-cost', 'uncachedUsd', 'Faktentiefe und Thorough Check: Kosten', 'USD ohne Cache'), ('settings-duration', 'durationSeconds', 'Faktentiefe und Thorough Check: Wartezeit', 'Sekunden'), ('settings-input', 'inputTokens', 'Faktentiefe und Thorough Check: Eingabetokens', 'Tokens')]:
            target = folder / (filename + '.svg')
            chart_metric(settings, target, metric, heading, unit)
            if png:
                subprocess.run(['rsvg-convert', str(target), '-o', str(target.with_suffix('.png'))], check=True)
            charts.append((filename, heading, 'Referenz: sol ohne Thinking. Jeweils wird nur Thorough abgeschaltet oder auf Titel als Faktentiefe gewechselt; Auswirkungen auf Qualität sind nicht bewertet.'))
    add('input-tokens', '5. Eingabemenge', 'Tokens hängen auch vom Tokenizer ab. Vergleiche zwischen Anbietern sind keine direkte Messung der Informationsmenge.', chart_metric, 'inputTokens', 'Wie viele Eingabetokens werden verarbeitet?', 'Tokens, Generierung + Prüfung')
    for audience in AUDIENCES:
        if not any(r[audience + 'Rendered'] for r in rows):
            continue
        add('length-' + audience, f'Textumfang · {audience}', 'Zeichen im gespeicherten Rendering, einschließlich Markdown. Länge und Zahl der Einträge messen keine Qualität oder Faktenabdeckung.', chart_metric, audience + 'Characters', f'Wie umfangreich sind die Texte? · {audience}', 'Zeichen', audience)
        add('flags-' + audience, f'Prüfermeldungen · {audience}', 'Eine Meldung ist keine bestätigte falsche Aussage. Weniger Meldungen können ebenso aus weniger Text oder einem anderen Prüfverhalten entstehen.', chart_metric, audience + 'Flags', f'Wie viele Meldungen werden ausgegeben? · {audience}', 'Meldungen', audience)
        target = folder / ('overlap-' + audience + '.svg')
        chart_overlap(rows, overlap, target, audience)
        if png:
            subprocess.run(['rsvg-convert', str(target), '-o', str(target.with_suffix('.png'))], check=True)
        charts.append(('overlap-' + audience, f'Wiederkehrende Meldungen · {audience}', 'Gezählt wird, welche PR in derselben Zielgruppe wiederholt Meldungen erhält. Die Begründung kann sich zwischen Läufen unterscheiden; Meldungen ohne PR-Zuordnung sind hier ausgeschlossen.'))
    add('cost-duration', 'Kosten und Wartezeit', 'Nur vollständige Läufe; die Legende nennt zusätzlich die Abschlussquote. Eine schnelle oder günstige Konfiguration ist damit noch keine gute Textkonfiguration.', chart_tradeoff)
    n_complete = sum(r['complete'] for r in rows)
    n_incomplete = sum(r['status'] == 'incomplete' for r in rows)
    n_missing = sum(not r['hasRecord'] for r in rows)
    observations = []
    cases = [c for c in CASE_ORDER if any(r['case'] == c for r in rows)]
    for case in cases:
        mine = [r for r in rows if r['case'] == case]
        observations.append(f"{CASE_NAMES[case]}: {sum(r['complete'] for r in mine)} von {len(mine)} Versuchen vollständig.")
    if name == 'october':
        observations += ['Im schwierigen Fall liefern OpenAI G-G und G-M jeweils keinen vollständigen Lauf von drei Versuchen.',
                         'Die Premiumkonfigurationen P-M sind nur für typisch und schwierig gemessen; für klein und groß fehlen Messungen.',
                         'Toolversion, Prompt, Faktentiefe und Thorough-Einstellung stimmen über die Records überein; Fakten und Release-Commits stimmen innerhalb jedes Szenarios überein.']
    if name == 'september':
        observations += ['Vierzehn Konfigurationen haben jeweils drei vollständige Läufe; zusätzlich bleibt ein fehlgeschlagener Versuch sichtbar.',
                         'Thinking, Prüfmodell, Thorough an/aus und Faktentiefe sind eigene Versuche an einem Release; ihre Wirkung wird nicht mit anderen Chartula-Versionen vermischt.',
                         'Lokale Modelle haben in der Preistabelle null API-Kosten; Hardware, Energie und Betrieb sind nicht eingerechnet.']
    if name == 'change-338':
        observations += ['Vorher und nachher haben jeweils zwei vollständige Läufe, unterschiedliche Chartula-Commits und unterschiedliche Prompt-Hashes.',
                         'Sechs weitere Versuchsfolder haben keinen Run-Record; ihre Dauer und Kosten bleiben unbekannt.',
                         'Eine historische Preistabelle für claude-sonnet-5 fehlt in diesen Sweep-Daten; deshalb erscheinen keine Kostencharts.']
    if name == 'october':
        for case in cases:
            candidates = [c for c in cells if c['case'] == case and c['complete'] == c['attempts'] == 3 and c['uncachedUsdMedian'] is not None]
            cheap = min(candidates, key=lambda c: c['uncachedUsdMedian'])
            fast = min(candidates, key=lambda c: c['durationSecondsMedian'])
            observations.append(f"{CASE_NAMES[case]}, unter den Konfigurationen mit 3/3 vollständigen Läufen: niedrigster Kostenmedian {cheap['label']} ({fmt(cheap['uncachedUsdMedian'], 4)} USD); niedrigster Laufzeitmedian {fast['label']} ({fmt(fast['durationSecondsMedian'], 1)} s).")
        observations.append('Diese Mediane beschreiben drei Wiederholungen; kleine Abstände sind keine belastbare Überlegenheit.')
    if name == 'september':
        lookup = {c['configuration']: c for c in cells}
        for model in ['gpt-6-luna', 'gpt-6-sol']:
            low, high = lookup[model + '-disabled'], lookup[model + '-high']
            observations.append(f"{model}, Thinking aus → hoch: Kostenmedian {fmt(low['uncachedUsdMedian'], 4)} → {fmt(high['uncachedUsdMedian'], 4)} USD; Laufzeitmedian {fmt(low['durationSecondsMedian'], 1)} → {fmt(high['durationSecondsMedian'], 1)} Sekunden.")
    limits = ['Die Ergebnisse beschreiben diese Releases und Einstellungen; sie sind keine allgemeine Modellrangliste.',
              'Einzelwerte und beobachtete Spannweiten zeigen Wiederholungen am selben Release, keine Konfidenzintervalle.',
              'Kosten mit fehlenden Nutzungsangaben sind Untergrenzen, falls costIsLowerBound gesetzt ist; daraus folgt kein vollständiger Gesamtpreis.',
              'Die Texte werden pro Konfiguration neu erzeugt; Prüferunterschiede können hier nicht isoliert werden.',
              'Judging und Rubriken bleiben eingefroren; es werden keine Qualitätsurteile erzeugt.',
              'Faktische Korrektheit, Vollständigkeit der Aussagen und Nachbearbeitungsaufwand wurden hier nicht bewertet.',
              'Kosten nach Cache sind anhand gespeicherter Nutzung und historischer Preise berechnet, nicht anhand einer Rechnung verifiziert.',
              'Pro Zielgruppe werden auch Texte teilweise vollständiger Läufe berücksichtigt; fehlende Texte sind keine leeren Texte.',
              'Lokale Arbeitsfassung: keine Rohtexte, Meldungsbegründungen oder Schlüsselkennungen im Export; Repository- und PR-Metadaten vor öffentlicher Veröffentlichung prüfen.']
    table_rows = [[CASE_NAMES[c['case']], c['label'], f"{c['complete']}/{c['attempts']}", fmt(c['uncachedUsdMedian'], 4), fmt(c['durationSecondsMedian'], 1), fmt(c['billedAllAttemptsUsd'], 4), fmt(c['billedSpendPerCompleteUsd'], 4)] for c in cells]
    headers = ['Szenario', 'Konfiguration', 'vollständig', 'Median USD ohne Cache', 'Median Sekunden', 'Cachekosten aller Versuche', 'Ausgaben / vollständige Läufe']
    body = f'<p class="eyebrow">Chartula · gespeicherte Messergebnisse</p><h1>{esc(title)}</h1><p class="intro">Vollständigkeit, API-Kosten, Wartezeit und Prüfermeldungen aus vorhandenen Läufen. Keine neue Generierung und keine Qualitätsbewertung.</p>'
    body += '<div class="cards">' + ''.join(f'<div class="card"><div class="number">{v}</div>{esc(t)}</div>' for v, t in [(len(rows), 'Versuche'), (n_complete, 'vollständig'), (n_incomplete, 'teilweise vollständig'), (n_missing, 'ohne Run-Record')]) + '</div>'
    body += '<h2>Was die Daten zeigen</h2><ul>' + ''.join(f'<li>{esc(o)}</li>' for o in observations) + '</ul>'
    body += '<p class="note">Prüfermeldungen sind Beobachtungen eines Prüfers. Ihre Zahl misst weder bestätigte Fehler noch Textqualität.</p>'
    md = [f'# {title}', '', 'Automatisch erzeugt durch `tools/sweep_results.py`; nicht von Hand bearbeiten.',
          'Lokale Auswertung vorhandener Messergebnisse, ohne Modellaufrufe und ohne Judging.', '',
          f'{len(rows)} Versuche; {n_complete} vollständig; {n_incomplete} teilweise vollständig; {n_missing} ohne Run-Record.', '',
          '## Beobachtungen', ''] + [f'- {o}' for o in observations]
    for filename, heading, description in charts:
        body += f'<h2>{esc(heading)}</h2><figure><a href="{filename}.svg"><img src="{filename}.svg" alt="{esc(heading + ": " + description)}"></a><figcaption>{esc(description)} <a href="{filename}.svg">SVG</a>' + (f' · <a href="{filename}.png">PNG</a>' if png else '') + '</figcaption></figure>'
        md += ['', f'## {heading}', '', description, '', f'![{heading}]({filename}.svg)']
    body += '<h2>Zahlen und Bezugsgrößen</h2>' + html_table(headers, table_rows)
    body += '<p class="small">Ausgaben / vollständige Läufe = Kosten aller Versuche geteilt durch die Zahl vollständiger Läufe. Nur bei vollständigem Kostenwissen und mindestens einem vollständigen Lauf berechnet; keine Prognose der Kosten einer Wiederholungsstrategie.</p>'
    body += '<h2>Szenarien und Eingabematerial</h2>'
    source_rows = []
    for case in cases:
        mine = [r for r in rows if r['case'] == case and r['hasRecord']]
        def unique(key):
            return ' / '.join(str(v) for v in sorted({r[key] for r in mine if r[key] is not None}, key=str)) or 'unbekannt'
        source_rows.append([CASE_NAMES[case], unique('pullRequests'), unique('facts'), unique('factsWithDescription'), unique('descriptionCharacters')])
    source_headers = ['Szenario', 'PRs', 'Fakten', 'Fakten mit Beschreibung', 'Beschreibungszeichen in den Fakten']
    body += html_table(source_headers, source_rows)
    body += '<p class="small">Größe allein beschreibt die Eingabe nicht: Der schwierige Fall hat kaum Beschreibungen. Angaben stammen aus Run-Records, nicht aus einer Größenabschätzung. Mehrere Werte zeigen unterschiedliche Faktentiefe innerhalb einer Reihe.</p>'
    body += '<h2>Konfigurationen und Herkunft</h2>'
    config_rows = []
    for config in ordered_configs(rows):
        mine = [r for r in rows if r['configuration'] == config and r['hasRecord']]
        first = mine[0]
        config_rows.append([first['label'], first['model'], first['thinking'], first['checkModel'] if first['thoroughCheck'] else 'aus', first['checkThinking'] if first['thoroughCheck'] else 'aus', first['factBaseDepth']])
    body += html_table(['Konfiguration', 'Generierung', 'Thinking', 'Prüfung', 'Check-Thinking', 'Faktentiefe'], config_rows)
    body += '<ul>' + ''.join(f'<li><code>{esc(v)}</code></li>' for v in sorted({r['toolVersion'] for r in rows if r['hasRecord']})) + '</ul>'
    body += '<p>Preisbasis: ' + (esc(price_path.name) + ', historisch unverändert übernommen.' if price_path else 'unbekannt.') + '</p>'
    body += '<h2>Grenzen und Methodik</h2><ul>' + ''.join(f'<li>{esc(t)}</li>' for t in limits) + '</ul>'
    body += '<h2>Daten herunterladen</h2><div class="downloads">' + ''.join(f'<a href="{f}">{f}</a>' for f in ['runs.csv', 'configurations.csv', 'flag-overlap.csv', 'data-issues.csv', 'report.md']) + '</div><p><a href="../index.html">Alle Vergleichsreihen</a></p>'
    md += ['', '## Zahlen', '', '| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |']
    md += ['| ' + ' | '.join(map(str, line)) + ' |' for line in table_rows]
    md += ['', 'Ausgaben / vollständige Läufe zählt alle Versuche, auch unvollständige und fehlgeschlagene.',
           'Bei unbekannten Kosten oder null vollständigen Läufen bleibt die Kennzahl unbekannt.', '',
           '## Konfigurationen', '', '| Konfiguration | Generierung | Thinking | Prüfung | Check-Thinking | Faktentiefe |', '| --- | --- | --- | --- | --- | --- |']
    md += ['| ' + ' | '.join(str(v) for v in line) + ' |' for line in config_rows]
    md += ['', '## Grenzen und Methodik', ''] + ['- ' + t for t in limits]
    md += ['', '## Daten', '', '- `runs.csv`: alle Versuche, fehlende Messwerte bleiben leer.', '- `configurations.csv`: Zusammenfassung mit definierten Nennern.', '- `flag-overlap.csv`: Meldungswiederholung je PR und Zielgruppe.', '- `data-issues.csv`: fehlende Records, Preise und widersprüchliche Metadaten.', '']
    (folder / 'report.md').write_text('\n'.join(md), encoding='utf-8')
    (folder / 'index.html').write_text(page(title, body), encoding='utf-8')
    return {'series': name, 'title': title, 'attempts': len(rows), 'complete': n_complete, 'incomplete': n_incomplete, 'withoutRecord': n_missing, 'charts': len(charts), 'issues': dict(Counter(i['kind'] for i in issues))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--png', action='store_true')
    args = parser.parse_args()
    if args.png and not shutil.which('rsvg-convert'):
        parser.error('--png requires rsvg-convert')
    repo, out = args.repo.resolve(), args.out.resolve()
    if out.exists() and any(out.iterdir()):
        marker = out / 'manifest.json'
        if not marker.exists() or json.loads(marker.read_text()).get('generatedBy') != 'sweep_results.py':
            parser.error('non-empty output is not managed by sweep_results.py')
    # Output must never replace an input sweep or the evaluation instrument.
    if out == repo or any(out == p or out in p.parents for p in (repo / 'sweeps').glob('*.json')):
        parser.error('output would overlap source inputs')
    sweeps = repo / 'sweeps'
    jobs = sorted(sweeps.glob('cmp-*.json'))
    inputs, summaries = {repo / 'tools' / 'sweep_stats.py'}, []
    series = [('october', 'Oktober 2026: vier reale Szenarien', [(p, json.loads(p.read_text())['case']['size'], None) for p in jobs], sweeps / 'prices-2026-10-09.json'),
              ('september', 'September 2026: Einstellungen an ServiceDeskLite', [(sweeps / 'servicedesklite-v1.9.0.json', 'typical', None)], sweeps / 'prices-2026-09-25.json'),
              ('change-338', 'Änderung #338: vorher und nachher', [(sweeps / f'chartula-338-{stage}.json', 'large', stage) for stage in ['before', 'after']], None)]
    for name, title, jobs, price_path in series:
        found = [(p, case, stage) for p, case, stage in jobs if p.exists() and (sweeps / p.stem).is_dir()]
        if found:
            summary = build_series(repo, out, name, title, found, price_path, inputs, args.png)
            if summary:
                summaries.append(summary)
    out.mkdir(parents=True, exist_ok=True)
    missing_plans = [p.name for p in sweeps.glob('*.json') if 'cells' in json.loads(p.read_text()) and not (sweeps / p.stem).is_dir()]
    manifest = {'schemaVersion': 1, 'generatedBy': 'sweep_results.py', 'generatorSha256': digest(Path(__file__)), 'series': summaries,
                'plansWithoutResults': sorted(missing_plans),
                'inputs': [{'path': str(p.relative_to(repo)), 'sha256': digest(p)} for p in sorted(inputs)]}
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    intro = '<p class="eyebrow">Chartula · Ergebnisaufbereitung</p><h1>Was die Vergleichsläufe zeigen</h1><p class="intro">Vorhandene Messungen verständlich aufbereitet. Jede Vergleichsreihe bleibt bei ihrer Versuchsanordnung und Version. Qualität wurde nicht bewertet.</p>'
    intro += '<div class="cards">' + ''.join(f'<div class="card"><h2><a href="{s["series"]}/index.html">{esc(s["title"])}</a></h2><p>{s["attempts"]} Versuche · {s["complete"]} vollständig · {s["charts"]} Charts</p></div>' for s in summaries) + '</div>'
    intro += '<h2>Wie die Ergebnisse gelesen werden</h2><ul><li>Abschlussquote zuerst; Kosten und Wartezeit danach.</li><li>Punkte zeigen einzelne Läufe; Median und beobachtete Spannweite ergänzen sie.</li><li>Meldungen sind keine bestätigten Fehler. Textumfang ist keine Qualität.</li><li>Historische Preise bleiben unverändert; berechnete Cachekosten sind keine verifizierte Rechnung.</li><li>Die Berichte bleiben lokal. Öffentliche Weitergabe braucht eine Prüfung der enthaltenen Repository- und PR-Metadaten.</li></ul>'
    intro += '<h2>Reproduzieren</h2><pre><code>python3 tools/sweep_results.py --out sweeps/results --png</code></pre><p>Kein Netzwerk, keine API-Kosten. SVG, HTML, Markdown und CSV benötigen nur Python; PNG zusätzlich rsvg-convert.</p><p><a href="manifest.json">Manifest mit Eingabeprüfsummen</a></p>'
    if missing_plans:
        intro += '<p class="note">Pläne ohne Ergebnisordner: ' + esc(', '.join(sorted(missing_plans))) + '. Keine Messwerte ergänzt.</p>'
    (out / 'index.html').write_text(page('Chartula: Vergleichsergebnisse', intro), encoding='utf-8')
    readme = ['# Vergleichsergebnisse', '', 'Automatisch erzeugt durch `tools/sweep_results.py`; nicht von Hand bearbeiten.',
              'Vorhandene Messwerte werden aufbereitet; Judging und Rubriken bleiben eingefroren.', '',
              '## Vergleichsreihen', '']
    readme += [f"- [{s['title']}]({s['series']}/report.md): {s['attempts']} Versuche, {s['complete']} vollständig, {s['charts']} Charts." for s in summaries]
    readme += ['', '## Reproduzieren', '', '```bash', 'python3 tools/sweep_results.py --out sweeps/results --png', '```', '',
               'SVG, HTML, Markdown und CSV benötigen nur Python.', 'PNG benötigt zusätzlich `rsvg-convert`.',
               'Die historische Preistabelle wird unverändert verwendet.',
               'Berechnete Kosten nach Cache sind nicht gegen eine Rechnung verifiziert.',
               'Alle Eingabedateien und ihre SHA-256-Prüfsummen stehen in `manifest.json`.',
               'Exports enthalten keine Schlüsselkennungen, Rohtexte oder Meldungsbegründungen.',
               'Repository- und PR-Metadaten vor öffentlicher Weitergabe prüfen.', '']
    (out / 'README.md').write_text('\n'.join(readme), encoding='utf-8')
    print(json.dumps(summaries, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
