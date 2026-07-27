# MGS Refactor Plan

Goals, in priority order: (1) behaviour preserved, (2) fewer generated `.mcfunction` files,
(3) less Python via de-duplication, (4) readability, (5) no in-game perf regression,
(6) no file over ~300 lines (revised down from ~500 on 2026-07-27).

Completed phases are summarised in §6; only their durable lessons are kept, in §7 and §8.

---

## 1. Verification harness

`scripts/verify.py` — one command, three modes:

```bash
python scripts/verify.py baseline      # build, then capture the reference snapshot
python scripts/verify.py check         # build, diff vs reference, run ruff + pyright, report deltas
python scripts/verify.py check --diff   # ... and print unified diffs of every changed file
python scripts/verify.py metrics       # metrics table only, no build
```

- Reference snapshot lives in `.refactor/baseline/` (gitignored, outside `build/`); it holds the full `datapack/` and `resource_pack/` trees. Zips and `sha1_hashes.json` are excluded — they are archives of the trees already compared.
- `check` exits non-zero if the output differs **or** ruff/pyright fail, so it gates a commit.
- `scripts/pyrightconfig.json` (`typeCheckingMode: strict`, `include: ../src`) makes `pyright -p scripts/pyrightconfig.json` reproducible without touching the IDE workspace root.
- **`build/` is git-tracked** and byte-deterministic, so `git status --porcelain build/` is a free second opinion.
- Build takes ~18–34 s.

**Re-baseline after every commit**, otherwise `check` reports the previous phase's work as drift.

---

## 2. Progress

| metric | Phase 0 (2026-07-24) | now | Δ |
|---|---:|---:|---:|
| Python files | 99 | 92 | −7 |
| Python LOC | 29 605 | 28 493 | −3.8 % |
| Generated `.mcfunction` files | 1 510 | 1 303 | **−13.7 %** |
| Generated command lines | 12 930 | 12 305 | −4.8 % |
| Comment lines in `src/` | 6 244 | 1 795 | **−71 %** |
| Resource pack | 173.7 MB | 103.8 MB | **−40 %** |
| `src/database/models/` | 32.2 MB | 18.3 MB | −43 % |
| ruff / pyright strict | 11 / 2 errors | **0 / 0** | ✅ |

### Generated functions by top-level group (Phase 0 census, for targeting)

`zombies` 749 · `multiplayer` 270 · `maps` 139 · `shared` 45 · `missions` 32 · `grenade` 30 ·
`ammo` 29 · `sound` 24 · `player` 24 · `mob` 22 · `dialogs` 20 · everything else 106.

`zombies` alone was 50 % of the output. Inside it: `pap` 105, `mystery_box` 98, `perks` 93,
root 77, `wunderfizz` 59, `wallbuys` 45, `powerups` 45, `revive` 28, `inventory` 27, `feedback` 26.

---

## 3. Remaining work

### D3. Cross-mode lifecycle duplication — **~20 files, ~600 Python LOC** (→ P10)

`multiplayer/`, `zombies/`, `missions/` each emit their own `summon_spawns`, `summon_spawn_iter`,
`summon_spawn_at`, `tp_all_to_spawns`, `pick_spawn`, `tp_to_spawn`, `tp_player_at`, `respawn_tp`,
`actual_respawn`, `announce_stats_iter`, `load_map_from_storage`, `setup`. Measured diff of
`multiplayer/summon_spawn_iter` vs `missions/summon_spawn_iter`: **identical except the mode segment
in three function paths and the comment lines.** Same for `tp_to_spawn`, plus one `@e`→`@n` selector
and the `mgs:<mode>` storage name.

The mode name is the only variable and is already known at the call site. Options: one
`shared/spawns/*` family taking `$(mode)`, or (better, no macro) a mode-agnostic body reading the
active mode's storage through a single `mgs:temp _mode` handle set once at game start.

**Savings: ~20 mcfunctions, ~600 Python LOC across the three `game.py` files. Risk: high** — this is
where behaviour drift is most likely. Ship one function-group per commit.

### PY5. Files over 300 lines — 26 of them (→ P12, final phase)

| file | lines | | file | lines |
|---|---:|---|---|---:|
| `functional/map_editor.py` | **1553** | | `missions/game.py` | 491 |
| `config/stats.py` | **1122** | | `loadouts/browsing.py` | 470 |
| `zombies/pap.py` | **985** | | `zombies/wallbuys.py` | 461 |
| `functional/shaders.py` | *950 — exempt* | | `functional/helpers.py` | 439 |
| `zombies/perks.py` | **939** | | `weapon/grenade.py` | 427 |
| `loadouts/editor.py` | **910** | | `zombies/inventory.py` | 396 |
| `zombies/mystery_box.py` | **740** | | `zombies/wunderfizz.py` | 386 |
| `multiplayer/game.py` | **737** | | `weapon/ammo.py` | 369 |
| `zombies/game.py` | **728** | | `weapon/raycast.py` | 367 |
| `zombies/round.py` | **621** | | `functional/main.py` | 340 |
| `zombies/revive.py` | **610** | | `zombies/escort.py` | 323 |
| `config/blocks.py` | **579** | | `loadouts/actions.py` | 315 |
| `zombies/powerups.py` | **572** | | `zombies/traps.py` | 307 |

`shaders.py` stays **one file** and stays exempt — its embedded GLSL is not decomposable. D3 shrinks
the three `game.py` files. Everything else splits.

The split is **by feature, not by kind**: a package per concept, holding the modules that only make
sense together.

```
zombies/
  perks/{registry,machine,effects}.py                # perks.py + wunderfizz.py — the machine and what it dispenses
  powerups/{types,spawn,collect}.py                  # powerups.py + bonus.py — the drop and the system that spawns it
  objects/{barriers,traps,wallbuys,doors,power}.py   # everything placed on a map
  pap/{machine,upgrade,anim,lore}.py
  mystery_box/{machine,pool,anim}.py
map_editor/{elements,markers,save,ui}.py
```

Each file is `generate_X()` emitting dozens of `write_versioned_function` blocks, so splitting means
carving one function into sub-functions across new modules and threading `ns` / `version` / `sep` and
the nested `snbt_*` helpers through every one. Large, invasive, zero output change — hence last, one
file per commit against the byte-identical harness.

### PY6. Generated-`.mcfunction` comment cleanup — ⚠ **needs sign-off**

A large share of the comments inside the emitted functions restate the following line
(`# Setup player`, `# Announce`, `# Next`). They live *inside* the f-strings passed to
`write_versioned_function`, so they are generated output: removing them moves
`mcfunction_total_lines` (31 675 vs 12 305 real commands) and cannot run under the byte-identical
harness without approval.

### PY8. Module-level helpers become class members (→ P11c)

Per the naming rule, module-level functions and constants group into a class with `@staticmethod`
methods. `functional/helpers.py` is the clearest case: everything except the genuinely global
`MGS_TAG` becomes `FunctionalHelpers.SPECIAL_SCORES`, `FunctionalHelpers.special_objectives_lines()`,
and so on. Sweep the other modules for the same shape afterwards. Pure renaming; risk very low but
the diff is wide.

### Lint tightening (→ P11)

Add `ANN`, `RET`, `SIM`, `PTH`, `TC`, `ARG`, `PL` to the ruff config and fix the fallout. Audit the
remaining `# noqa` / `type: ignore` / `cast(` / `Any` occurrences while there.

---

## 4. Target file tree (remaining deltas only)

```
src/
  functional/
    shaders.py                   # UNCHANGED, exempt from the size rule — GLSL stays inline
    helpers.py                   # → FunctionalHelpers class (PY8)
    core/
      spawns.py                  # NEW — the one spawn system all three modes call (D3)
    zombies/
      perks/, powerups/, objects/, pap/, mystery_box/    # PY5 feature packages
    map_editor/{elements,markers,save,ui}.py             # was map_editor.py
```

---

## 5. Risks and how each is verified

| risk | why it is hard | mitigation |
|---|---|---|
| **Cross-mode lifecycle (P10)** | A shared spawn system must reproduce three subtly different behaviours (team vs FFA vs mission spawn selection, `@e` vs `@n`, the zombies-only `new_spawn` tag). The diff will be large and hard to eyeball. | One function group per commit. Show the before/after generated pair side by side. Manual in-game test of each mode's spawn + respawn + late-join before merging. |
| **PY5 silent drift (P12)** | Carving one big `generate_X()` into modules touches every emitted f-string; a dropped line is invisible in review. | Byte-identical harness after every single file. One file per commit. |
| **`auto.lang_file` couples strings to output** | Any whitespace or case change in a displayed string silently changes generated lang keys. | The harness diffs the lang file. Do not retype strings; move them. |
| **Beet `Mem.ctx` is pipeline-only** | Reading `Mem.ctx` at import time crashes. | Load data at module import (no `Mem` needed); resolve `ns` / `version` only inside generate-time functions. |
| **Registration order is load-bearing** | Reordering `Mem.definitions` moves every downstream artefact — loot tables, item models, lang keys. | Never reorder a definitions table, even to group it more logically. |

---

## 6. Completed phases

| # | phase | output Δ | Python Δ |
|---|---|---:|---:|
| **P1** ✅ | Fix the 11 ruff + 2 pyright errors that existed at Phase 0. | 0 | +12 |
| **P2** ✅ | Fix `auto.headers` in **StewBeet** to scan dialogs (StewBeet `9517e97b`). 113 headers gained real callers; `@within ???` 114 → 90. | 0 files, 113 headers | +45 (StewBeet) |
| **P3** ✅ | Merge `database/*.py` into `items.py`; delete `_template.py`, the dead `export_all_definitions_to_json` tail, `definitions_debug.json`, `game_mode.py`, `generator.py`. | 0 | −240, −8 files |
| **P4** ✅ | 97 `_zoom` models became `parent:` children. **RP 173.7 → 103.8 MB.** Equivalence proved by resolving parent chains and deep-comparing: 485/485 identical. | intentional diff | +8 |
| **P5a** ✅ | Inlined the 26 `zombies/feedback/sound_*` into a `zb_sound()` table; `shared/maps/call_*_script_at_base` ×6 → 1 macro. | −31 | −31 |
| **P5b** ⛔ | Dropped, with a −5 salvage of genuinely dead redirects. See §8. | −5 | −26 |
| **P6a** ✅ | Mystery-box give 32 → 2, PaP `apply_field` 28 → 1 macro, wunderfizz `set_model`+`grant` 28 → 0, admin powerups 11 → 1. | −95 | −29 |
| **P6b** ✅ | Perks `pool/try_index` 14 → 1, `pool/count` deleted, `powerups/spawn_type` 11 → 1, `mob/default/level_*` 5 → 0, `set_door_link_*` 8 → 2. | −35 | −45 |
| **P7** ✅ | One shared `zombies/deny/message` + `deny/not_enough_points`. D6 dropped. | −29 | −93 |
| **P8** ✅ | Loadout editor: one shared `show_static_dialog` skeleton for 13 submenus, 4 dead `scope/*` aliases deleted. | −18 | +1 |
| **P9a** ✅ | `stats.py` sound dedup + magazine single-sourcing; perk & power-up typed registries. | 0 | −599 |
| **P9b** ✅ | `ALL_ELEMENTS` / `EDITOR_MODES` → dataclasses; definitions split into `map_editor_defs.py`. | 0 | +1 file |
| **P9c** ✅ | Codebase-wide comment/docstring cleanup. Comments 2922 → 1795. | 0 | −813 |
| **P9d** ✅ | Restored the 211 `# Imports` / `# Constants` / `# Classes` / `# Functions` section banners P9c wrongly deleted. | 0 | +211 |
| **P11b** ✅ | PY7 — `catalogs.py`'s six tuple-splat tables became explicit keyword-argument constructor calls. | 0 | +1 |
| **P11a** ✅ | Indentation normalised to tabs across 30 files (26 were space-indented, 5 mixed). Alignment padding and non-docstring string interiors left as spaces. | 0 | 0 |

### Remaining phases

| # | phase | output Δ | Python Δ | risk |
|---|---|---:|---:|---|
| **P10** | D3 — one shared spawn/respawn system for all three modes. | −~20 | −600 | **high** |
| **P11** | Tighten the ruff config, fix the fallout. | 0 | ? | low |
| **P11c** | PY8 — `helpers.py` and friends fold into `FunctionalHelpers`-style classes. | 0 | ~0 | very low |
| **P12** (final) | PY5 — split every >300-line generator into feature packages. **Not** `shaders.py`. | 0 | +~45 files | med |

---

## 7. Gotchas worth keeping

- **`return run` takes exactly one command.** `execute unless <cond> run return run function .../deny_x` cannot be inlined when `deny_x` has two commands — the second would silently never fire, and a byte-diff would look plausible. This is what killed P5b's `deny_*` family.
- **`auto.lang_file`'s `TEXT_RE` matches any `text:"…"` textually,** leftmost match wins, and duplicate base keys get a `_2` suffix by scan order. Never name a macro argument `text` — with `text:'{"text":"Nuke",…}'` it translates the *outer* quoted value and mints junk keys like `mgs.text_nukecolor_redbold_true`. Use `msg`, `label`, etc.
- **Registration order in `database/items.py` is load-bearing.** Splitting the 14 perk machines into two loops reorders `Mem.definitions` and moves every downstream artefact.
- **Reading beet's `dialog.data` rewrites the file.** The `.data` getter calls `ensure_deserialized()`, which replaces the stored content with the parsed form, so the dialog is re-encoded on output and loses its hand-written formatting. Scan `.text` for read-only analysis.
- **PEP 701:** an f-string replacement field can contain lines of Python code (see the `late_join_flow_lines(...)` call inside `zombies/join_game`), mixed with mcfunction body lines in the same string. Any bulk reindent must protect `FSTRING_START..FSTRING_END` spans wholesale.
- **A macro cannot re-quote its own argument**, so `value:"$(value)"` and `value:$(value)` need separate entry points.
- **Re-read line numbers immediately before a line-range edit.** A stale range deleted `SPECIAL_SCORES` from `helpers.py` during P9c; only the build failure caught it.
- **Dialogs are load-time resources** — a `/reload` is needed to see edits in game.

## 8. Do not re-attempt

- **`kicks/type_{0..5}{,_ds}` (12) and `sound/{cycle,fire_alt,fire_simple,pump}`** — the hottest path in the pack (every shot). Collapsing needs either a per-shot macro or 60 `execute if score` evaluations instead of ~10. Both slower.
- **`_1`…`_4` scope models** — 40–170 real geometry elements each, not duplication.
- **D1 inlining beyond P5a (P5b).** Of 104 candidates, **87 would be absorbed into a function reachable from `#minecraft:tick`** (`zombies/game_tick` alone would take 10, and it is already 90 commands). The brief rejects that. The other 17 remove indirection, not duplication.
- **D6 map-editor per-mode families.** `save_lists/zombies` clears 12 element lists, `missions` clears 6; `give_tools` hands out a different toolbar per mode. They already come from **one** loop over a shared table, so there is no Python duplication either. Same for `players/row_{mode}`.
- **`perks/apply/*` (14)** — each is an effect plus a **static** `tellraw`. Parameterising the message turns the translate components into macro text and the pack silently loses 14 translation keys.
- **`perks/reapply/*` (10)** — bodies are already deduplicated `commands` lists; inlining duplicates all 10 across **two** call sites.
- **`revive/hud_*` (4) and `mystery_box/hud_*` (5)** — warm paths (downed-player tick, hover tick) *and* 2-command `return run` targets.
- **`zombies/types/*` (5)** — not a duplication family; `normal`/`dog` genuinely differ and the rest already delegate.
- **Static dialog resources with a `score` component (P8 part 2).** Dialogs are a synced registry rendered client-side, so a `score` component has no resolution context. None of the 23 shipped dialogs uses one.
- **Slot parameterisation of `equip1`/`equip2` and `primary`/`secondary` (P8 part 3).** Each merge is −1 file for +2–3 command lines at the call site — it moves duplication into callers.
- **Aggregate near-duplicate clustering numbers.** A token-set Jaccard pass said "123 redundant files"; a `difflib` pass said "313". They disagree by 2.5×. Every per-family count above was verified by reading the generated files; the clustering aggregates are not a metric.

---

## 9. Standing decisions

1. **No data files for definitions.** Weapon stats, block tags and shaders stay as Python.
2. **Dialog resource changes are acceptable**, including the `/reload`-to-update semantics.
3. **`@within ???` is not evidence of an orphan** — that was the `auto.headers` bug fixed in P2.
4. **Zoom models use vanilla `parent:` inheritance** rather than a build-time merge.
5. **The size threshold is ~300 lines**, revised down from ~500 on 2026-07-27.
6. **`shaders.py` stays one file** and keeps its exemption. Reaffirmed twice.
7. **Section banners are mandatory** — `# Imports`, `# Constants`, `# Classes`, `# Functions` are structure, not commentary.
8. **Splitting is by feature, not by kind** — a package per concept, holding the modules that only make sense together.
9. **No `_`-prefixed names anywhere.** Everything in this codebase is public.
10. **Dataclass tables use one explicit constructor call per row**, never a tuple splat.
11. **A reduction only counts if it eliminates duplication** or replaces generated variants with data-driven logic. Concatenating unrelated files, or inlining a hot loop into one enormous function, does not count.
12. **StewBeet may be edited. `beet` must not be touched.**
