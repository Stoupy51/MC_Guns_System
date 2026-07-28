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

### Finding duplication

```bash
npx jscpd ./src/functional -r ai --mode mild
```

Clone detection over the Python side. `--mode mild` catches near-duplicates rather than only exact
copies, which is what matters here — most duplication in this tree is the same emitter written twice
with different literals. Use it to *find* candidates, then verify each one by reading the files: the
Phase 0 clustering passes disagreed by 2.5x, so no similarity tool's aggregate is a metric (see §8).

---

## 2. Progress

| metric | Phase 0 (2026-07-24) | now | Δ |
|---|---:|---:|---:|
| Python files | 99 | 296 | +199 |
| Python LOC | 29 605 | 31 276 | +5.6 % |
| Largest non-exempt file | 1 553 | **300** | **−81 %** |
| Generated `.mcfunction` files | 1 510 | 1 305 | **−13.6 %** |
| Generated command lines | 12 930 | 12 328 | −4.7 % |
| Comment lines in `src/` (at P9c) | 6 244 | 1 795 | **−71 %** |
| Resource pack | 173.7 MB | 103.8 MB | **−40 %** |
| `src/database/models/` | 32.2 MB | 18.3 MB | −43 % |
| ruff / pyright strict | 11 / 2 errors | **0 / 0** | ✅ |

Python LOC and file count both went **up** in P12b, and that is the intended trade. A package leaf
costs a docstring, an import block and a `def` line that the monolith did not pay; 296 files at ≤300
lines each is the goal, not a smaller total. The metric that matters is the third row.

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

### PY5. Files over 300 lines — ✅ done (P12b, 2026-07-27)

Every non-exempt file is now **≤300 lines**. The 26 oversized files at Phase 0 became feature packages;
`functional/shaders.py` (1097) keeps its exemption and stays one file.

`functional/zombies/maps.py` sits at exactly 300 and was left alone: it is a flat map registry with no
seam worth cutting, and 300 is the threshold, not past it.

The split was **by feature, not by kind** — a package per concept, holding the modules that only make
sense together. That part mattered as much as the line counts: `functional/zombies/` was 27 modules in
one flat directory and `functional/weapon/` was 15, both unnavigable regardless of individual size.

**How the carve worked.** Each oversized file was one `generate_X()` emitting dozens of
`write_versioned_function` blocks. A scratchpad tool sliced it by line range, moved every body line
verbatim (so no emitted command was ever retyped), derived each new module's imports from the tokens
its slice actually uses, and bumped relative import levels by one. Locals shared across sections were
handled in a **separate prep commit** before the carve — promoted to module level when they were pure
derivations, or listed in a preamble the tool hands back to only the slices that read them.

**Prep commits worth remembering,** because each removed real duplication rather than just moving code:

- `ZombiesCommon.gun_cd(ns)` — the `{ns}:{gun:true}` predicate was written out in three files.
- `SlotPredicates` — `inventory.py`'s eleven parallel `*_slot_cd` locals became one frozen dataclass.
- `owned_gun_macro_cd(ns)`, `MB_CLOSED_TF` / `MB_OPEN_TF` — mystery box, used across four sections.
- `editor_fn(ns, version)` + a module-level `write_static_dialog` — the loadout editor's dialog filler.
- `normalize_btn_fields(ns)` / `compute_trig(ns, …)` — shared by both loadout browsers.
- `SEP`, `ZB_ELEMENTS`, `snbt_suggest` / `snbt_compound` — map editor, used end to end.

**`helpers.py` was different in kind.** It is a class, not a generator, so slicing it by line range
would have left one class spread over six files. Instead `FunctionalHelpers` became six classes —
`SpecialScores`, `GameLifecycle`, `SharedContent`, `RankedStats`, `Text`, `Dialogs` — and all 156
call sites were repointed at the class that now owns each member. `MGS_TAG` is *defined* in
`helpers/__init__.py` (not re-exported from it), so its ~30 importers were untouched.

### PY6. Generated-`.mcfunction` comment cleanup — ⚠ **needs sign-off**

A large share of the comments inside the emitted functions restate the following line
(`# Setup player`, `# Announce`, `# Next`). They live *inside* the f-strings passed to
`write_versioned_function`, so they are generated output: removing them moves
`mcfunction_total_lines` (31 675 vs 12 305 real commands) and cannot run under the byte-identical
harness without approval.

### PY8 remainder — the flat stat vocabularies

`config/stats/{keys,casings,colors,sounds}.py` are deliberately **not** classed. They are flat name
vocabularies: `CAPACITY`, `DAMAGE`, `PAP_STATS` and ~90 siblings, read directly inside the weapon
tables. `StatKeys.CAPACITY` would appear ~900 times there for no type-checking gain. Overrule this if
you disagree — it is the one place the "group helpers into a class" rule was knowingly not applied.

**Rule established while doing this:** a module whose only top-level function *is* its entry point
stays a module. Wrapping `generate_power_switch()` in a class buys nothing. Classing applies to
modules other modules import *helpers* from.

### PY9. Clones jscpd found once the splits landed — 1 done, 4 open

`npx jscpd ./src/functional --mode mild --min-lines 8 --min-tokens 60` reports **0.42 %** duplication
(11 clones, 118 lines). Six of them are inside `shaders.py` and are GLSL, not logic. The rest, ranked:

1. ✅ **`projectile/explode.py` ≡ `grenade/detonate.py`** — done. `weapon/explosion.py` now owns
   `Explosion.setup_lines()` (the 16-line centre/config/shooter block) and `Explosion.area_damage_lines()`
   (2 more lines both paths repeated). Output byte-identical: both generators still emit their own copy,
   the Python is written once. The shared-mcfunction variant was **not** taken — it would have cut ~19
   generated lines but added a file, and goal (2) is *fewer* generated files.
   Left alone: the `on_explosion` signal block, 3 shared lines whose only difference is one extra
   `.grenade` field. Folding it needs a boolean flag parameter, which reads worse than the repetition.
2. **`pap/purchase.py` [44-55] vs [145-156]** — 12 lines, 211 tokens. The re-PaP-at-max-level path and
   the full upgrade path share their cosmetic-roll tail.
3. **`wallbuys/give.py` [67-81] vs [223-237]** — 15 lines, the gun and the knife give paths.
4. **`revive/hooks.py` [11-25] vs [28-42]** — 15 lines, the game-start and game-stop resets.
5. **`pap/free.py` [46-54] vs `pap/purchase.py` [117-125]** — 9 lines, the shared upgrade tail again.

Verify each by reading before acting: jscpd's aggregate is not a metric (§8), and these are emitters
whose "duplication" is sometimes two genuinely different commands that happen to tokenize alike.

### Lint tightening (→ P11)

Add `ANN`, `RET`, `SIM`, `PTH`, `TC`, `ARG`, `PL` to the ruff config and fix the fallout. Audit the
remaining `# noqa` / `type: ignore` / `cast(` / `Any` occurrences while there.

---

## 4. Target file tree (remaining deltas only)

Only D3 still moves files:

```
src/
  functional/
    core/
      spawns.py                  # NEW — the one spawn system all three modes call (D3)
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
| **P11c** ✅ | PY8 — `helpers.py`'s 26 members folded into `FunctionalHelpers`; `MGS_TAG` stays module-level. 15 consumers repointed. | 0 | +1 |
| **P11d** ✅ | PY8 — `feedback.py`→`ZombiesFeedback`, `zombies/common.py`→`ZombiesCommon`, `core/spawning.py`→`CoreSpawning`, `core/weapon_drop.py`→`WeaponDrop`, `classes.py`→`MultiplayerClasses`. All 31 `_`-prefixed names stripped codebase-wide. | 0 | +5 |
| **P12a** ✅ | PY5 moves — 33 modules regrouped into 9 feature packages (`zombies/{game,player,enemies,machines,objects,rewards}`, `weapon/{firing,ammo,hud}`). 32 files had relative imports rewritten. | 0 | +9 files |
| **P12b-1** ✅ | `config/stats.py` (1122) → 13-module package, all under 300 lines. `ItemBuilder`/`PapStats` classed; 28 consumers repointed at the owning submodule. | 0 | +13 files |
| **P12b-2** ✅ | `config/blocks.py` (581) → 6-module package, one per tag family. | 0 | +5 files |
| **P12b-3** ✅ | Generator splits, one package per file, each its own commit: `main`, `weapon/grenade`, `firing/raycast`, `objects/{traps,barriers,wallbuys}`, `loadouts/actions`, `zombies/game/{round,lifecycle}`, `multiplayer/game`, `player/revive`, `ammo/magazine`, `machines/wunderfizz`, `missions/game`, `rewards/powerups`. | 0 | +~70 files |
| **P12b-4** ✅ | The five big ones: `machines/mystery_box` (941), `machines/perks` (1072), `machines/pap` (1198), `loadouts/editor` (1031), `map_editor` (1848). Each preceded by a prep commit hoisting its cross-section locals. | 0 | +~60 files |
| **P12b-5** ✅ | The tail: `loadouts/browsing`, `player/inventory`, `enemies/escort`, `firing/projectile`, `ammo/lore`. | 0 | +~25 files |
| **P12b-6** ✅ | `helpers.py` (546) → six classes by concern; 156 call sites repointed. `SPECIAL_SCORES` → `SpecialScores.ALL` (one generated comment line changed, approved). | 1 line | +6 files |

### Remaining phases

| # | phase | output Δ | Python Δ | risk |
|---|---|---:|---:|---|
| **P10** | D3 — one shared spawn/respawn system for all three modes. | −~20 | −600 | **high** |
| **P11** | Tighten the ruff config, fix the fallout. | 0 | ? | low |
| **PY6** | Generated-`.mcfunction` comment cleanup. Needs sign-off — it moves output. | −~19 000 lines | 0 | low |

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
- **A file-level `# ruff: noqa` can sit below a long module docstring.** A carve that only scans the first dozen lines for lint directives will drop it and bury the new modules in E501. Scan to the end of the docstring instead.
- **A slice boundary must be re-derived after any prep commit.** Promoting constants shifts every line number below it, and a boundary landing inside a triple-quoted f-string fails as `TokenError: unterminated triple-quoted f-string literal` — which at least fails loudly. A boundary landing in a *gap* between slices silently drops definitions and only shows up as `F821`.
- **A module-level header must get its own slice.** `wunderfizz`, `powerups`, `perks`, `escort` and `pap` each carry constants or a dataclass above the generator; without a `func=""` slice for that block the package raises `NameError` at import.
- **Only top-level imports get their relative level bumped.** A function-local `from ..config… import x` inside a moved file is invisible to an `ast.parse` over `tree.body`, and surfaces as a `ModuleNotFoundError` at build time. `ast.walk` instead, or grep for indented `from ..` after every carve.
- **Splitting a long function exposes shadowed dead code.** `powerups.py` had a `display_name` assignment that pyright could not flag while an earlier loop in the same 570-line function bound the same name; the split made it a clean unused-variable error.

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
