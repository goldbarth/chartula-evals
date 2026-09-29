# Evaluation: comparison runs ServiceDeskLite v1.9.0

As of: 2026-09-25.
Case: `goldbarth/ServiceDeskLite` `v1.9.0 --since 675555a7` (v1.7.0), 19 commits, 18 facts, `--no-publish`.
Chartula: `0.1.0-preview.3+7620e6d` in all 43 attempts.
14 cells with 3 valid runs each, 1 failed attempt (granite cell).
All numbers from the run records, produced with `python3 tools/sweep_stats.py report sweeps/servicedesklite-v1.9.0 sweeps/prices-2026-09-25.json`.
Tables, raw data and charts: `sweeps/servicedesklite-v1.9.0-stats/` (`report.md`, `runs.csv`, `flags.csv`, `cells.csv`, `flags-by-pr.csv`, `axis-a.svg`, `axis-b.svg`).
Costs: OpenAI list price, standard tier, reference date 2026-09-25 (`sweeps/prices-2026-09-25.json`), without cache, so the run order does not shift the numbers.
Every number is the median of 3 runs, min-max in parentheses.

## What the data does not support

- n = 3 per cell. Differences of one flag per run lie within the range in every cell; they are not a finding.
- The flag count says nothing about whether a flag is justified, and nothing about the quality of the texts. The texts were not scored against the rubric. I read the flag texts for axis B and the local cells, for axis A only #233.
- One case, one release, one kind of repository. Release size is not measured (decided for budget reasons).
- terra is not measured (decided: weaker than sol, one generation older, more expensive on output than gpt-6-sol).

## Axis A: render model and thinking (check: gpt-6-sol, disabled)

| Render | Thinking | Cost $ | of which rendering $ | Reasoning tokens | Duration s | Flags/run |
|---|---|---|---|---|---|---|
| gpt-6-luna | disabled | 0.0512 (0.0510-0.0512) | 0.0029 | 0 | 32 (30-35) | 4 (3-4) |
| gpt-6-luna | low | 0.0521 (0.0511-0.0530) | 0.0033 | 803 (644-926) | 43 (39-45) | 4 (3-5) |
| gpt-6-luna | medium | 0.0545 (0.0515-0.0549) | 0.0054 | 4,608 (3,074-6,103) | 72 (55-83) | 4 (2-6) |
| gpt-6-luna | high | 0.0552 (0.0550-0.0574) | 0.0075 | 8,879 (8,276-10,994) | 128 (124-137) | 3 (3-4) |
| gpt-6-sol | disabled | 0.1048 (0.1047-0.1055) | 0.0569 | 0 | 40 (39-40) | 3 (3-4) |
| gpt-6-sol | low | 0.1055 (0.1044-0.1066) | 0.0578 | 69 (63-76) | 48 (47-51) | 4 (2-5) |
| gpt-6-sol | medium | 0.1181 (0.1124-0.1286) | 0.0707 | 1,319 (581-2,167) | 76 (69-94) | 3 |
| gpt-6-sol | high | 0.1701 (0.1635-0.1859) | 0.1230 | 6,252 (5,510-7,680) | 170 (161-208) | 3 |

The check on gpt-6-sol costs $0.048 per run in every cell; for luna it is over 90 % of the cost.

**Answer.**
Thinking does not lower the flags at any level: all eight cells sit at 3 or 4 flags per run, the ranges overlap.
Thinking raises duration and cost: for sol, going from `disabled` to `high` raises cost by 62 % ($0.105 to $0.170) and duration 4.3-fold (40 to 170 s); for luna, duration 4-fold (32 to 128 s) at nearly the same cost.
The best ratio of cost to flags belongs to **gpt-6-luna with `disabled`**: $0.051 including the check, of which $0.003 for rendering, 32 s, 4 (3-4) flags, versus sol `disabled` at $0.105, 40 s, 3 (3-4) flags.
The one-flag difference between luna and sol does not hold at n = 3.
Not confirmed: whether luna and sol write equally good texts. The flag count does not measure that.

The most stable flag depends on the fact, not the model: #233 is flagged in 7 of 8 cells in 3 of 3 runs (luna `medium`: 2 of 3).
Reason according to the flag text: #244 removed the implementation from #233 again, #245 reintroduced the badges; the fact base still lists #233 as a change of its own.

## Axis B: render × check (thinking `disabled` for both)

| Render ↓ / checked by → | gpt-6-luna | gpt-6-sol |
|---|---|---|
| gpt-6-luna | **6**, technical 0, customer 6 (self-check) | 4 (3-4), technical 1, customer 3 (2-3) |
| gpt-6-sol | 5 (4-8), technical 0, customer 5 (4-8) | **3 (3-4)**, technical 1 (1-2), customer 2 (self-check) |

**Answer.**
The flags depend on the checker, more than on the renderer: luna as checker reports 6 and 5 flags per run, sol as checker 4 and 3.
luna as checker flags only the customer view (0 technical flags in 6 runs); sol flags at least one technical entry in every one of its runs.
Part of luna's surplus is not a finding: at least 7 of the 35 luna flags say in their own reasoning that the passage is supported ("The wording is supported.", "Supported by [#222]."). With sol as checker: none of 88 flags across all sol-checked cells (searched by text pattern, every hit read).
Does a model check itself more leniently? The data does not show that: luna checks itself with 6 flags, sol's text with 5; sol checks itself with 3 (3-4), luna's text with 4 (3-4). The one-flag difference for sol lies within the same range.
Cost: luna as checker $0.0025 instead of $0.048 per run.

## Side axes (against `gpt-6-sol-disabled`: $0.1048, 40 s, 3 (3-4) flags)

| Cell | Input tokens | Cost $ | Duration s | Flags/run |
|---|---|---|---|---|
| Reference `gpt-6-sol-disabled` | 43,751 | 0.1048 | 40 | 3 (3-4), technical 1 (1-2), customer 2 |
| thorough off | 21,293 | 0.0572 | 34 | 0 |
| `factBase.depth: title-only` | 5,876 | 0.0230 | 29 | 1 (1-2), technical 0, customer 1 (1-2) |

**thorough.**
Without the thorough check no run reports a flag: the rule-based check found nothing in all 42 runs of the sweep.
With thorough on gpt-6-sol, 3 (3-4) flags per run are added, for $0.048 (+83 % cost) and 6 s more per run.
Whether that pays off depends on how many of the flags are justified; that is not assessed here. The flag review of 2026-09-24 found false alarms (ROADMAP, section "Geparkt aus der Flag-Review").
What is established: without thorough, #233, for example, goes unnoticed in this case, although it is flagged in 3 of 3 reference runs and, according to the flag text, describes an already removed implementation as a change.

**factBase.depth.**
`title-only` lowers input tokens by 87 % and cost by 78 %, flags from 3 to 1.
Fewer flags here means less material, not better texts: without a description there is less for the text to overstretch. What the texts lose in content is not measured.

**Release size.** Not measured.

## Local: qwen3:14b renders (Ollama 0.33.3, RTX 4080 SUPER, `num_ctx 24576`)

| Cell | Attempts | Duration s | of which check s | Flags/run | notEvaluated |
|---|---|---|---|---|---|
| checked by qwen3 | 3 / 3 | 90 (71-97) | 32 | 17 (0-28) | 0 |
| checked by granite | 3 / 4 | 219 (48-677) | 164 | 3 (0-4) | 0 (1 in the failed attempt) |

Cost $0 (electricity and hardware not accounted for).

**qwen3:14b as renderer: no.**
In 7 attempts: once Chartula rejected the customer rendering ("an entry for fact 18, which it was not sent"); once (`qwen3-14b-checked-by-qwen3-14b/run-2`) the example from the prompt ("Saving over a network drive") appeared as an entry in `release-v1.9.0.md`.
None of the 36 GPT runs contains a prompt example in its output (text search for both example labels).

**qwen3:14b as checker: no.**
0, 28 and 17 flags in three runs; in the run with 17 flags, 13 say "The facts support this claim" in their reasoning.
It did flag the invented network-drive entry, though (3 flags).

**granite4.1-guardian:8b as checker: no.**
It follows the response schema formally (`notEvaluated` 0 in the valid runs), but not in substance: 2 of 7 flags contain a `<think>` log instead of a reasoning.
One check call failed on a `finish_reason` the SDK does not know; another took 618 s with one retry.
One run ended with 0 flags after 40 output tokens.

## Decision memo: open launch items

Observed on 2026-09-25 with the installed preview.3; nothing is decided.

1. **`install.sh` completion message names only Anthropic: confirmed.**
   Wording: "Chartula needs two keys": `ANTHROPIC_API_KEY`, `GITHUB_TOKEN`. OpenAI needs a key, provider, base URL and model.
2. **Token write permission before the first model call: not observable today** (`--no-publish`).
   No up-front check found in the preview.3 code (searched for `permission`, `403` in `Cli/Commands`, `Core/Pipeline`); the evidence remains the finding from 2026-09-23.
   Related: the token could not see the private repo (HTTP 404); noticed through my verification command, not through Chartula. How Chartula reports this is not tested.
3. **Docs "Using another provider": needed.**
   Required today and written down nowhere as a recipe: `Chartula__Llm__Provider=openai-compatible`, `Chartula__Llm__BaseUrl=https://api.openai.com/v1` (no default), `OPENAI_API_KEY`, a valid model ID (`gpt-6-terra` does not exist), `num_ctx` for Ollama.
   The missing base URL only surfaced in the sweep plan through your question.
   A typo in the variable name (`OPEN_API_KEY`) went unnoticed because another valid key was set; Chartula cannot detect that.
4. **`chartula init` / `chartula doctor`: would have saved steps today.**
   Checked by hand: installed version (no `--version`), base URL, model ID, the token's read access to the repo, Ollama model present, Ollama context window.
   Each of these would otherwise only have surfaced during the run; whether Chartula's message then names cause and fix is not checked.
5. **Small issues:** the #210 class occurred again today: the header line says "key from OPENAI_API_KEY", although the variable was not set.
