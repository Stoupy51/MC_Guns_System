# MGS Refactor Plan — Phase 0 audit

**Status: Phase 0 complete (audit only, no refactoring code written). Awaiting review.**

Goals, in priority order: (1) behaviour preserved, (2) fewer generated `.mcfunction` files,
(3) less Python via de-duplication, (4) readability, (5) no in-game perf regression,
(6) no file over ~500 lines.

---

## 1. Verification harness

`scripts/verify.py` — one command, three modes:

```bash
python scripts/verify.py baseline      # build, then capture the reference snapshot
python scripts/verify.py check         # build, diff vs reference, run ruff + pyright, report deltas
python scripts/verify.py check --diff   # ... and print unified diffs of every changed file
python scripts/verify.py metrics       # metrics table only, no build
```

- Reference snapshot lives in `.refactor/baseline/` (gitignored, outside `build/`); it holds the
  full `datapack/` and `resource_pack/` trees. Zips and `sha1_hashes.json` are excluded — they are
  archives of the trees already compared.
- `check` exits non-zero if the output differs **or** ruff/pyright fail, so it gates a commit.
- Also added: `scripts/pyrightconfig.json` (`typeCheckingMode: strict`, `include: ../src`) so
  `pyright -p scripts/pyrightconfig.json` is reproducible; it does not affect the IDE workspace root.
- **`build/` is git-tracked**, so `git status --porcelain build/` is a free second opinion. Verified
  the build is byte-deterministic: two consecutive builds produced zero changed files.
- Build takes ~18–34 s.

Baseline captured and `check` confirmed **`✅ output is byte-identical to the baseline`**.

---

## 2. Baseline numbers (2026-07-24, v5.1.0)

| metric | value |
|---|---:|
| Python files (`src/**.py`) | **99** |
| Python LOC | **29 605** |
| Generated `.mcfunction` files | **1 510** |
| — of which contain a macro line (`$…`) | 356 (24 %) |
| Generated command lines (non-comment, non-blank) | **12 930** |
| Generated `.mcfunction` total lines (incl. headers) | 34 038 |
| Datapack JSON files | 755 (609 are per-item loot tables from stewbeet) |
| Resource-pack JSON files | 2 293 (1 142 models + 1 142 items, plugin-generated) |
| Datapack size | 19.1 MB |
| Resource-pack size | 173.7 MB |
| `src/database/models/*.json` | **288 files, 32.2 MB** |
| ruff (`--config ../stouputils/pyproject.toml`) | **11 errors** ❌ |
| pyright strict | **2 errors** ❌ |

Neither linter is currently clean — see P1.

### Generated functions by top-level group

| group | files | | group | files |
|---|---:|---|---|---:|
| `zombies` | **749** | | `mob` | 22 |
| `multiplayer` | **270** | | `dialogs` | 20 |
| `maps` | **139** | | `players` | 16 |
| `shared` | 45 | | `kicks` | 15 |
| `missions` | 32 | | `raycast` | 14 |
| `grenade` | 30 | | `projectile` | 13 |
| `ammo` | 29 | | `utils` | 12 |
| `sound` | 24 | | `switch` | 11 |
| `player` | 24 | | everything else | 35 |

`zombies` alone is 50 % of the output. Inside it: `pap` 105, `mystery_box` 98, `perks` 93,
root 77, `wunderfizz` 59, `wallbuys` 45, `powerups` 45, `revive` 28, `inventory` 27, `feedback` 26.

### Prior work (context)

A previous refactor round (commits `b880a91c`…`e261dade`) converted generators to classes, then
**reverted 54 of them**, and explicitly scoped itself to *byte-identical output*. Its conclusion —
"the three modes' lifecycle bodies genuinely diverge, so they can't be shared" — was correct
**under that constraint**. This round is allowed intentional, explained output diffs, so that
conclusion no longer blocks the work. `src/functional/generator.py` (`McfunctionGenerator`) and
`game_mode.py` (`GameMode`) are the surviving remnants; both are near-empty and are candidates
for deletion once their two shared helpers move elsewhere.

---

## 3. Duplication inventory — mcfunction side

Ordered by payoff. Counts are measured from `build/`, not estimated.

### D1. Single-command wrapper functions — **~140 files** ⭐ biggest single lever

**291 of 1 509 generated functions contain exactly one command**; 149 of those are macros (must
stay separate — a macro needs its own function), leaving **142 plain one-command functions**.
Of those, **74 have exactly one known caller** (read from the `@within` headers stewbeet emits)
and 30 are public entry points (`@within ???`) that must stay.
There are a further **151 two-command non-macro functions, 110 with exactly one known caller**.

Worst offender: `zombies/feedback/sound_*` — **26 files, each a single `playsound`**:
```
# zombies/feedback/sound_deny.mcfunction
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0
```
Callers do `function mgs:v5.1.0/zombies/feedback/sound_deny`. Inlining the `playsound` at each
call site removes 26 files **and** one function dispatch per use — a small runtime *win*, not a
cost. Single-sourcing moves to Python: a `ZOMBIE_SOUNDS: dict[str, str]` table plus a
`zombies_sound(name, target)` line-builder, so the sound is still declared exactly once.

Same shape in `maps/*/calls/` (11), `multiplayer/editor/scope/` (4), `zombies/escort` (3), …

`shared/maps/call_{join,leave,power,respawn,start,tick}_script_at_base` (6 files) belongs here too:
five identical commands plus one `data modify … _base.fn set value "#mgs:maps/<x>_script"`. The
caller can emit those five lines inline — **no macro**, which matters because
`call_tick_script_at_base` runs every tick. **−5.**

**Savings: ~145 mcfunctions, ~0 Python LOC (the bodies move into the callers' f-strings).**
**Risk: low-medium.** Per-case check needed where the caller uses `return run function X` or
`execute if … run function X` with a 2-command body (the guard must then be repeated).

### D2. Per-entity function families — **~130 files**

| family | files | collapses to | saves | path |
|---|---:|---|---:|---|
| `zombies/pap/apply_field/*` | 28 | 1 macro | 27 | cold (PaP purchase) |
| `zombies/mystery_box/default_give/*` | 32 | 1 | 31 | cold (box roll) |
| `zombies/perks/pool/try_index/*` | 14 | 1 macro | 13 | cold (perk roll) |
| `zombies/wunderfizz/grant/*` | 14 | 1 macro | 13 | cold |
| `zombies/wunderfizz/set_model/*` | 14 | 1 macro | 13 | cold (spin anim, ~1/tick during a spin) |
| `zombies/perks/apply/*` + `reapply/*` | 24 | ~4 | ~20 | cold |
| `zombies/powerups/spawn_type/*` | 11 | 1–2 | ~9 | cold |
| `zombies/admin/powerup_*` | 11 | 1 macro | 10 | cold (admin menu) |
| `mob/default/level_*` (two dirs) | 9 | ~2 | ~7 | cold |
| `maps/editor/set_door_link_*` | 7 | 2 macros | 5 | cold (map editor) |
| `zombies/admin/round_skip_*`, `points_add_*` | 6 | 2 macros | 4 | cold (admin menu) |
| `zombies/revive/hud_{gold,red,white,yellow}` | 4 | 1 macro | 3 | **warm** — downed-HUD tick |
| `maps/editor/save_{point,spawn,*_command}` | 4 | ~2 | 2 | cold |
| `zombies/mystery_box/hud_{moving,ready,spinning}` | 3 | 1 macro | 2 | cold |
| `zombies/types/{armed,fast,tank}` | 3 | 1 | 2 | check callers first — likely tag targets |

All eight bodies differ only in literals that the caller *already has in storage*. Examples:

```mcfunction
# zombies/pap/apply_field/damage      (×28, only the field name changes)
data modify storage mgs:temp _pap_pick.list set from storage mgs:temp _pap_extract.stats.pap_stats.damage
execute if data storage mgs:temp _pap_pick.list[0] run function mgs:v5.1.0/zombies/pap/pick_list_value
...

# zombies/mystery_box/default_give/ak47   (×32, only the weapon id / mag id / count change)
data modify storage mgs:temp _wb_weapon set value {weapon_id:"ak47",name:"ak47",consumable:0b,magazine_id:"ak47_mag",mag_count:3}
scoreboard players set #wb_price mgs.data 0
function mgs:v5.1.0/zombies/wallbuys/process_purchase with storage mgs:temp _wb_weapon
```

```mcfunction
# zombies/admin/powerup_max_ammo      (×11, 6 commands, only the last-but-one line changes)
execute unless data storage mgs:zombies game{state:"active"} run return run tellraw @s [...]
tag @s[scores={mgs.zb.in_game=1},gamemode=!spectator] add mgs.pu_collecting
...
function mgs:v5.1.0/zombies/powerups/activate/max_ammo
tag @a[tag=mgs.pu_collecting] remove mgs.pu_collecting
```
→ one macro ending in `$function mgs:v5.1.0/zombies/powerups/activate/$(type)`.

`mystery_box` is the cleanest: `mystery_box_pool` **already carries** `weapon_id`, `magazine_id`,
`mag_count`, `consumable` per entry, and each `default_give/<w>` just restates them. The picker can
copy the chosen entry straight into `_wb_weapon` and call `process_purchase` — no macro at all.
⚠ `give_function` is a documented per-map data hook (custom pools point at their own function), so
the field must survive; only the 32 *default* ones go away.

**Savings: ~160 mcfunctions. Risk: low** except `zombies/revive/hud_*`, which runs from the
downed-player HUD tick — 4 unique argument sets, so the macro cache is warm after the first frame,
but measure it rather than assume.

⚠ **Not in this group:** `sound/{cycle,fire_alt,fire_simple,pump}` cluster together but run once per
shot. Same reasoning as `kicks/` (D7) — leave them static.

### D3. Cross-mode lifecycle duplication — **~20 files, ~600 Python LOC**

`multiplayer/`, `zombies/`, `missions/` each emit their own `summon_spawns`, `summon_spawn_iter`,
`summon_spawn_at`, `tp_all_to_spawns`, `pick_spawn`, `tp_to_spawn`, `tp_player_at`, `respawn_tp`,
`actual_respawn`, `announce_stats_iter`, `load_map_from_storage`, `setup`. Measured diff of
`multiplayer/summon_spawn_iter` vs `missions/summon_spawn_iter`: **identical except the mode
segment in three function paths and the comment lines.** Same for `tp_to_spawn` (plus one
`@e`→`@n` selector and the `mgs:<mode>` storage name).

The mode name is the only variable, and it is already known at the call site. Options: one
`shared/spawns/*` family taking `$(mode)`, or (better, no macro) a mode-agnostic body that reads
the active mode's storage through a single `mgs:temp _mode` handle set once at game start.

**Savings: ~20 mcfunctions, ~600 Python LOC across the three `game.py` files (934 + 873 + 645).**
**Risk: high** — this is where behaviour drift is most likely. Ship last, one function-group per
commit.

### D4. Loadout-editor slot parallelism — **~25 files, ~300 Python LOC**

`multiplayer/editor/` is 88 files, riddled with `primary`/`secondary`/`equip1`/`equip2` copies:
`pick_equip_slot1|2`, `pick_equip1|2_camo`, `hub_row_equip1|2`, `append_equip1|2`,
`show_equip{1,2}_camo_dialog{,_macro}`, `show_equip_slot{1,2}_dialog{,_macro}`,
`show_scope_primary_{full,no4,1only}`, `show_secondary_{pistol,overkill}_dialog`, …

Two separate wins:

1. **13 `show_*_dialog` wrappers are byte-identical except the macro they call:**
   ```mcfunction
   function mgs:v5.1.0/multiplayer/editor/recompute_points
   execute store result storage mgs:temp _pts int 1 run scoreboard players get @s mgs.mp.edit_points
   function mgs:v5.1.0/multiplayer/editor/show_<X>_dialog_macro with storage mgs:temp
   ```
   Hoist the first two lines into one `editor/prepare_points`; callers then run
   `prepare_points` + the macro directly. **−12 files.**
2. The 13 matching `_macro` functions exist *only* to interpolate `$(_pts)` into an otherwise
   static dialog. A registered dialog resource can render that number with a
   `{"score":{"name":"@s","objective":"mgs.mp.edit_points"}}` component instead — no macro, no
   function. `helpers.py::register_dialog` already does exactly this pattern elsewhere.
   **−13 files** (they become dialog JSON resources, not mcfunctions).
3. Slot-parameterising the remaining equip1/equip2 and primary/secondary pairs: **−~8 files**.

**Savings: ~25–30 mcfunctions, ~300 Python LOC. Risk: medium** (dialog rendering is user-visible;
verify the points number and layout are pixel-identical in game).

### D5. `zombies/deny_*` — **~13 files**

34 `deny_*` functions; six are `deny_not_enough_points` differing only in **which score holds the
price** (`#pap_price`, `#pk_price`, `#zb_mystery_box_price`, …), four are `deny_requires_power`,
and `deny_moving` / `deny_all_owned` / `deny_not_your_result` / `deny_in_use` each appear twice
(mystery box + wunderfizz). Writing the price into one `#deny_price mgs.data` before the call
collapses each set to one shared function under `zombies/deny/`.

**Savings: ~13 mcfunctions. Risk: low** (cold, chat-feedback only).

### D6. Map-editor per-mode families — **~10 files**

`maps/editor/{create,list,save_lists,give_tools,summon_existing}/{multiplayer,zombies,missions}` —
15 files, 3 per operation, generated by `for mode_key, mode_info in EDITOR_MODES.items()` loops.
Measured near-identical. One macro each driven by `$(mode)`. Also `players/list_{mode}` +
`players/row_{mode}` (6 → 2).

**Savings: ~10 mcfunctions, ~120 Python LOC. Risk: low.**

### D7. `kicks/` — **12 files, NOT recommended**

*(Applies equally to `sound/{cycle,fire_alt,fire_simple,pump}`, flagged in D2.)*

`kicks/type_{0..5}{,_ds}` is a 6×5 numeric recoil table. It is on the **hottest path in the pack**
(every shot). Collapsing it needs either a per-shot macro (slower) or one big flat function with
60 `execute if score` evaluations instead of ~10 (slower). Listed here so it is not re-discovered
later: **leave it alone.** If anything, the *Python* generator is already compact and data-driven.

---

## 3b. Upstream bug — `stewbeet.plugins.auto.headers` ignores dialogs ⚠ blocks P5

`FunctionAnalyzer` (`StewBeet/python_package/stewbeet/plugins/auto/headers/function_analyzer.py`)
builds `@within` from exactly three sources: `ctx.data.function_tags`, `ctx.data.advancements`, and
regex scans of mcfunction bodies. **`ctx.data.dialogs` is never read.** Any function reachable only
from a dialog button is therefore reported as an orphan:

```mcfunction
#> mgs:v5.1.0/maps/editor/menu
# @within	???          ← wrong
```
```json
// build/datapack/data/mgs/dialog/v5.1.0/config.json
{"action": {"type": "run_command", "command": "/function mgs:v5.1.0/maps/editor/menu"}}
```

This is not cosmetic for this refactor: **P5 (D1) classifies inlining candidates by caller count
read from `@within`.** With dialogs invisible, functions that *are* called look like public entry
points, and — worse — a function whose only caller is a dialog could be wrongly judged "orphan" and
deleted. The fix must land **before** P5, and P5's caller census must be re-run afterwards.

**Fix:** add `analyze_dialogs()` alongside `analyze_advancements()`, walking each dialog's JSON
recursively for string values containing `/function <ns>:<path>` (the `run_command` /
`suggest_command` action commands), and record the reference as `dialog <dialog_path>` — mirroring
the existing `advancement <path>` convention. Reuse `FUNCTION_CALL_RE`. Add a doctest in the same
style as the existing ones in that file, and check whether any other `ctx.data` resource type can
carry a command string while there.

Note this fix **changes the generated output**: many `@within ???` headers gain real caller lists.
That is a comment-only diff, but a large one, so it gets its own phase and its own re-baseline.

**Repo: StewBeet (editing allowed). `beet` must not be touched.**

---

## 4. Duplication inventory — Python side

### PY1. Definitions stay in Python — restructure, don't relocate

> **Decided (2026-07-24):** no TOML/JSON data files for definitions. Weapon stats, block tags and
> shaders stay as Python. **`shaders.py` is explicitly exempt from the ~500-line rule** — its 755
> lines of embedded GLSL stay where they are and the file may be as big as it needs to be.

So the win here is *not* moving ~2 400 lines to data files. It is removing repetition **within**
`config/stats.py` (1 418 lines, ~1 120 of which are 30 near-identical per-weapon stat dicts):

- The 30 weapon dicts repeat the same ~25 keys with the same shape every time, and each carries a
  hand-written `PAP_STATS` block that repeats the same sub-keys again.
- Every weapon also restates its `BASE_WEAPON` as its own id, and `database/ammo.py` **re-declares
  all 24 magazine capacities** that `CAPACITY` already holds in `stats.py` — a genuine
  single-source-of-truth hazard, not just noise.

Target: a frozen `WeaponDef` dataclass (see PY4) with sensible defaults and a `pap:` sub-dataclass,
so each weapon declares only what differs from the default. Still Python, still readable as a
table, but ~40 % shorter and `pyright --strict`-checked. `config/blocks.py` gets the same treatment
where its tag lists share entries.

**Savings: ~450 Python LOC, `stats.py` drops under 1 000. Risk: very low** (harness proves the
emitted `custom_data` is unchanged).

### PY2. `src/database/models/*.json` — **97 files, ~14.6 MB** ⭐

288 JSON files, 32.2 MB. Measured across all 102 `<w>_zoom.json` / `<w>.json` pairs:
**97 differ from their base *only* in the `display` block** — every `elements`, `textures`, and
`groups` entry is a duplicate of the base file (90–130 KB each). The 5 exceptions
(`mac10_zoom`, `spas12_zoom`, `vz61_zoom`, `g3a3_1_zoom`, `g3a3_3_zoom`) have real element or
texture differences and stay as full files.

The `display` values are hand-tuned per weapon (94 distinct blocks across 102 files) so they are
**not** derivable — but they are the *only* thing that differs.

> **Decided (2026-07-24): use vanilla model inheritance,** not a build-time merge. Each zoom model
> becomes a real child model:
> ```json
> { "parent": "mgs:item/ak47", "display": { "firstperson_righthand": { … } } }
> ```
> Minecraft resolves `parent` at resource-pack load: the child inherits `elements`, `textures` and
> `gui_light` from the parent, and its `display` entries override the parent's per slot. This is
> strictly better than merging in Python — it shrinks the **generated resource pack** too, not just
> the source tree.

This means the resource-pack output **will change** (each zoom model drops from 90–130 KB to a few
hundred bytes), which is an intentional, explained diff — the first one in the plan.

Verification for this phase is therefore *not* "byte-identical". It is:
1. Every `<w>_zoom.json` in the built pack resolves to the same effective model as the baseline
   (script: resolve `parent` chains in both trees and deep-compare the flattened result).
2. In-game visual check of iron-sight and ADS views on a handful of weapons across the affected
   families (one full-scope weapon, one shotgun, one pistol).

⚠ Two things to check during implementation: that `stewbeet.plugins.resource_pack.item_models` and
the iso-render generator both follow `parent` (the renders currently skip `_zoom` variants, so this
is likely a non-issue), and that the 5 real exceptions (`mac10_zoom`, `spas12_zoom`, `vz61_zoom`,
`g3a3_1_zoom`, `g3a3_3_zoom`) stay as full standalone models.

The `_1`…`_4` scope variants are **not** derivable — they add 40–170 real geometry elements each
(scope attachments). Leave them as standalone files.

**Savings: 97 source files, ~14.6 MB of source, and a comparable cut from the 173.7 MB resource
pack. Risk: low-medium** (output diff is by design; correctness is verified by parent resolution +
an in-game look).

### PY3. `src/database/*.py` — 8 files doing one job

`ammo.py`, `casing.py`, `grenades.py`, `others.py`, `rpg7.py`, `weapons.py`, `camo.py`,
`_template.py` are all "declare items". `_template.py` is dead scaffolding (a 25-line
`add_item("template", …) × 10` block that ships nothing) — **delete it**; a `WeaponDef` dataclass
with defaults replaces the reason it existed. `ammo.py` hand-lists 24 magazine capacities that
already exist in `config/stats.py` as `CAPACITY` — a real single-source-of-truth bug waiting to
happen.

**Target: `database/items.py` (registration) + `database/camo.py` (image pipeline, genuinely
different) + `src/data/*.{json,toml}`. Savings: ~5 files, ~150 LOC.**

### PY4. Typed registries instead of `dict[str, JsonDict]`

`zombies/perks.py::PERK_DEFINITIONS`, `map_editor.py::ALL_ELEMENTS` / `EDITOR_MODES`,
`zombies/powerups.py`, `zombies/wallbuys.py` are all string-keyed dicts of untyped dicts read by
`d["display_name"]` all over. `config/catalogs.py` already does this **right** with frozen
dataclasses — extend that pattern. This is what makes `pyright --strict` actually verify the data
instead of trusting it, and it is a prerequisite for D2 (a generic emitter needs a typed row).

### PY5. Files over 500 lines — 19 of them

`map_editor.py` 2054, `config/stats.py` 1418, `shaders.py` 1290, `zombies/pap.py` 1241,
`zombies/perks.py` 1106, `loadouts/editor.py` 1058, `multiplayer/game.py` 934,
`zombies/mystery_box.py` 928, `zombies/game.py` 873, `zombies/round.py` 788, `zombies/revive.py` 738,
`zombies/powerups.py` 687, `missions/game.py` 645, `config/blocks.py` 605, `zombies/wallbuys.py` 581,
`loadouts/browsing.py` 573, `weapon/grenade.py` 540, `helpers.py` 536, `zombies/escort.py` 510.

PY1 fixes three of them outright. D3/D4 shrink four more. The rest split by concern
(e.g. `pap.py` → `pap/{machine,upgrade,anim,lore}.py`).

### PY6. Misc

- `functional/generator.py::McfunctionGenerator` now provides only `ns`/`version` properties and
  two `load`/`tick` wrappers carrying a `# type: ignore[arg-type]`. Per the standing preference,
  call `write_load_file` / `write_tick_file` directly and delete the class along with
  `game_mode.py` once its two helpers move to `core/`.
- `setup_definitions.py` ends with a bare `return` before a live `export_all_definitions_to_json`
  call — dead code, delete (and `definitions_debug.json`, a 1.4 MB tracked artefact).
- `helpers.py` mixes tabs and spaces between functions (ruff `E101` fires in `zombies/ability.py`).
- 62 `# noqa`, 7 `type: ignore`, 14 `cast(`, 15 `Any` — audit each in the lint phase.
- 6 244 comment lines over 29 605 LOC (21 %). A large share restate the following line
  (`# Setup player`, `# Announce`, `# Next`); those also leak into the generated `.mcfunction`
  files and inflate `mcfunction_total_lines` (34 038 vs 12 930 real commands).

---

## 5. Proposed target file tree

```
src/
  config/
    schema.py                    # NEW — WeaponDef / PapDef / PerkDef frozen dataclasses (PY1/PY4)
    stats.py                     # stat KEY constants + PAP helpers + the weapon table, as WeaponDefs
    catalogs.py                  # unchanged — already the model the rest should copy
    blocks.py                    # unchanged in kind; de-duplicated tag lists
  database/
    models/
      *.json                     # bases + scope variants (full) and 97 tiny `parent:` zoom children
    items.py                     # was ammo/casing/grenades/others/rpg7/weapons.py
    camo.py                      # unchanged — image pipeline, a genuinely separate concern
  functional/
    shaders.py                   # UNCHANGED and exempt from the size rule — GLSL stays inline
    emit.py                      # NEW — shared command/line builders (was helpers.py + generator.py)
    dialogs.py                   # NEW — dialog registration helpers, split out of helpers.py
    core/
      spawns.py                  # NEW — the one spawn system all three modes call (D3)
      deny.py                    # NEW — shared deny/feedback functions (D5)
      ...                        # bounds, teleport, map_loading, commands, spawning as today
    weapon/                      # unchanged — already data-driven via storage, low duplication
    zombies/
      pap/{machine,upgrade,anim,lore}.py     # was pap.py (1241)
      perks/{registry,machine,effects}.py    # was perks.py (1106)
      ...
    multiplayer/
      loadouts/editor/{hub,pick,dialogs}.py  # was editor.py (1058)
    map_editor/{elements,markers,save,ui}.py # was map_editor.py (2054)
scripts/
  verify.py, pyrightconfig.json  # the harness
```

One-line justifications: `config/schema.py` is where `pyright --strict` gets to check the
definitions (which stay Python, per the decision above); `functional/core/spawns.py` and `deny.py`
are where the cross-cutting duplication lands; the `pap/`, `perks/`, `editor/`, `map_editor/`
splits exist purely to get those four files under 500 lines along concern lines that already exist
inside them; `emit.py` replaces the near-empty `generator.py` + `game_mode.py`. `shaders.py` is
deliberately left alone.

---

## 6. Phased work plan

Each phase is one commit, independently shippable, verified with
`python scripts/verify.py check` before it is checked off.

| # | phase | output Δ | Python Δ | risk |
|---|---|---:|---:|---|
| ~~**P1**~~ ✅ | Fix the 11 ruff + 2 pyright errors that exist today. No behaviour change. | **0 (byte-identical)** | +12 | none |
| ~~**P2**~~ ✅ | §3b — fix `auto.headers` in **StewBeet** to scan dialogs. Re-baselined (comment-only diff). **Unblocks P5.** | 0 files, 113 headers | +45 (StewBeet) | low |
| ~~**P3**~~ ✅ | PY3/PY6 — merge `database/*.py` into `items.py`; delete `_template.py`, the dead `export_all_definitions_to_json` tail, `definitions_debug.json`, `game_mode.py`. | **0 (byte-identical)** | −181, −7 files | low |
| ~~**P4**~~ ✅ | PY2 — 97 `_zoom` models become `parent:` children. First intentional output diff; verified by parent-resolution compare. | **−69.9 MB RP**, 0 files added/removed | +8 | low-med |
| **P5a** ✅ | D1 — inlined the 26 `zombies/feedback/sound_*`; `shared/maps/call_*_script_at_base` ×6 → 1 macro. | **−31** | −31 | low |
| **P5b** ⚠ | D1 remainder — **re-scoped to 108** (see below), and demoted below P6 on value-per-edit. | −~108 | ~0 | low-med |
| **P6a** ✅ | D2 — mystery box give, PaP apply_field, wunderfizz set_model+grant, admin powerups. | **−95** | −29 | low |
| **P6b** ✅ | D2 remainder — perks `pool/try_index` + `pool/count`, `powerups/spawn_type`, `mob/default/level_*`, `set_door_link_*`. Four families dropped as bad value (see below). | **−35** | −45 | low |
| **P7** ✅ | D5 — shared `zombies/deny/message` + `deny/not_enough_points`. **D6 dropped**, its premise was wrong (see below). | **−29** | −93 | low |
| **P8** | D4 — loadout editor: `prepare_points`, static dialog resources with score components, slot parameterisation. | −~28 | −300 | medium |
| **P9** | PY1/PY4/PY5 — `WeaponDef` dataclasses, typed registries, split the remaining >500-line files (**not** `shaders.py`), delete restating comments. | 0 | −850, +12 files | low |
| **P10** | D3 — one shared spawn/respawn system for all three modes. | −~20 | −600 | **high** |
| **P11** | Tighten the ruff config (add `ANN`, `RET`, `SIM`, `PTH`, `TC`, `ARG`, `PL`), fix the fallout. | 0 | ? | low |

**Projected end state: ~1 130–1 180 `.mcfunction` files (−23 %), ~26 000 Python LOC (−12 %),
~85 Python files, `src/database/models` down from 32.2 MB to ~17.6 MB, and a materially smaller
resource pack.** (The Python figure is less ambitious than the Phase 0 draft: definitions stay in
Python by decision, and `shaders.py` keeps its 755 GLSL lines.)

> **On the aggregate similarity numbers:** I ran two near-duplicate clustering passes over the
> generated tree — a token-set Jaccard pass (≥ 0.8 → "123 redundant files") and a `difflib`
> sequence-ratio pass (≥ 0.88 → "313"). They disagree by 2.5×, so **treat neither aggregate as a
> metric.** Every per-family count in §3 was verified by reading the actual generated files; those
> are exact. The projection above is built only from the verified families.

Order rationale: P1 and P3 are zero-output-change and prove the harness on real edits. P2 comes
early because P5's caller analysis is wrong until it lands. P4 is the first intentional diff and is
small and self-contained, so it is a good place to exercise the "explain the diff" workflow. P5 and
P6 are the two biggest mcfunction wins and are mechanical. P10 is the largest structural change and
the one most likely to drift, so it lands only after the harness has been exercised nine times.

---

## 7. Risks and how each is verified

| risk | why it is hard | mitigation |
|---|---|---|
| **Cross-mode lifecycle (P10)** | A shared spawn system must reproduce three subtly different behaviours (team vs FFA vs mission spawn selection, `@e` vs `@n`, the zombies-only `new_spawn` tag). A diff will be large and hard to eyeball. | Convert one function group per commit, not the whole system. For each, show the before/after generated pair side by side. Manual in-game test of each mode's spawn + respawn + late-join before merging. |
| **Macro cost on warm paths (P6)** | `wunderfizz/set_model` runs during a spin animation (roughly once per tick while spinning). A macro recompiles per unique argument set — 14 sets here, so it caches, but the first spin pays. | State the path class for every conversion. If a family turns out to be warmer than assumed, keep it static and say so rather than pushing through. |
| **`give_function` is a public data hook (P6)** | Custom maps ship their own mystery-box pools with their own `give_function` paths. Removing the field would break them. | Keep the field and its contract; only the 32 built-in default functions collapse. Explicitly re-read `zombies/mystery_box.py` + `wallbuys.py` for other data-driven function references before touching it. |
| **Inlining changes control flow (P5)** | `return run function X` and `execute if … run function X` do not inline mechanically when `X` has two commands. | Classify every call site from the `@within` headers first; inline only the single-caller, single-command cases automatically, and handle the rest by hand. |
| **Dialog resources render differently (P8)** | Swapping a macro-built dialog for a static resource with a `score` component is not something the diff can validate — the JSON *will* differ by design. | Ask before starting P8. Screenshot the before/after of each affected menu in game. Dialogs are load-time resources, so a `/reload` is needed to see edits. |
| **Model key ordering (P3)** | Rebuilding `_zoom` models as `base` merged with `override` can reorder JSON keys and change the resource-pack bytes even though the pack behaves identically. | Apply the override in place on a copy of the base so key positions are preserved; require byte-identical output, not "equivalent". |
| **`auto.lang_file` couples strings to output** | Any whitespace or case change in a displayed string silently changes generated lang keys. | Already covered — the harness diffs the lang file. Do not retype strings; move them. |
| **Beet `Mem.ctx` is pipeline-only** | Reading `Mem.ctx` at import time crashes. New data-loading code in P2 must stay lazy. | Load `src/data/*` at module import (no `Mem` needed), but resolve `ns`/`version` only inside generate-time functions. |
| **Not everything reducible is worth reducing** | `kicks/` (D7) and the `_1`…`_4` scope models look like duplication but are not. | Recorded above so they are not re-attempted. |

---

## 8. Review decisions (2026-07-24)

1. **No data files for definitions.** Weapon stats and block tags stay as Python. PY1 becomes
   "restructure with dataclasses", not "move to TOML". ✅ answered
2. **Dialog resource changes are acceptable** (P8), including the `/reload`-to-update semantics.
   ✅ answered
3. **`@within ???` is not evidence of an orphan** — `auto.headers` is broken (§3b). Fix it in
   StewBeet rather than reasoning around it. ✅ answered → new P2
4. **Delete `definitions_debug.json`** and the dead generator tail. ✅ answered → P3
5. **`shaders.py` is exempt from the ~500-line rule** and keeps its GLSL inline. ✅ answered
6. **Zoom models use vanilla `parent:` inheritance** rather than a build-time merge. ✅ answered

---

## Changelog

- **2026-07-24** — Phase 0 complete. Harness built and verified, baseline captured, plan written.
  Nothing refactored yet.
- **2026-07-24** — A second, slower clustering pass surfaced 7 more verified duplicate families
  (`zombies/admin/powerup_*` ×11, `shared/maps/call_*_script_at_base` ×6,
  `maps/editor/set_door_link_*` ×7, `mob/default/level_*` ×9, `zombies/revive/hud_*` ×4,
  `maps/editor/save_*` ×4, `zombies/mystery_box/hud_*` ×3, `zombies/types/*` ×3). D1/D2 estimates
  raised from ~270 to ~305 files; projection revised to −23 %. Also recorded that the two
  clustering methods disagree 2.5× and neither aggregate should be used as a metric.
- **2026-07-24** — Plan reviewed and approved to start. Six decisions recorded in §8: definitions
  stay in Python, `shaders.py` exempt from the size rule, zoom models use `parent:` inheritance,
  dialog resource changes accepted, `definitions_debug.json` deleted, and the `auto.headers` dialog
  bug (§3b) promoted to P2 because P5's caller analysis depends on it. Phases re-ordered
  accordingly; Python LOC target revised from −19 % to −12 %.
- **2026-07-24** — **P1 done.** ruff and pyright strict both clean; output byte-identical.
  Fixes: `roaming.py` unused `version`; `feedback.py` ambiguous `×` → `x`; `ability.py` 4 mixed
  tab+space continuation indents → tabs; `inventory.py` `slot: int` (line 305) collided with
  `for slot in ALL_SLOTS` (`str`) in the same function scope — the numeric one is now `perk_slot`;
  `perks.py` two >200-char emitted lines split into named locals (`ts_marker`, `ts_nearby_alive`);
  `main.py` the identical 6-line lethal-damage preamble that both `signal_and_damage` variants
  repeated is now one `lethal_handoff` local.
  **Python LOC +12** — the E501 fixes cost more lines than the `main.py` de-duplication saved.
  Worth noting the metric can move the "wrong" way for a correct change; P1 was about
  correctness, not size.
- **2026-07-24** — **P2 done.** `analyze_dialogs()` added to StewBeet's `FunctionAnalyzer`
  (StewBeet commit `9517e97b`), plus a doctest and an integration-test regression guard.
  Result on this pack: **113 headers changed, 0 command bodies changed**, `@within ???`
  **114 → 90** (24 false orphans resolved), 81 functions gained an `@executed` context.

  Two things the first attempt got wrong, both caught by the harness:
  1. Reading `dialog.data` reformatted **9 dialog JSON files**. beet's `.data` getter calls
     `ensure_deserialized()`, which *replaces* the file's stored content with the parsed form, so
     the dialog is re-encoded on output and loses its hand-written formatting. Fixed by scanning
     `.text` instead — same encoder beet writes with, so analysis stays read-only.
  2. Running the dialog pass *before* `analyze_function_calls()` downgraded the `@executed` of 5
     functions that have both a dialog and an mcfunction caller (e.g. `multiplayer/auto_assign_team`
     lost `as @a[scores={mgs.mp.in_game=1}]` in favour of the generic player context), because
     `ContextAnalyzer` returns on the first recognised caller. Fixed by running dialogs last.

  **Remaining 90 `@within ???` are now trustworthy** — that census is what P5 depends on.
- **2026-07-24** — **P3 done.** Output byte-identical; **99 → 92 Python files, −181 LOC**.
  - `game_mode.py` folded into `generator.py` (both are generator bases, 61 lines total). The
    `load`/`tick` wrapper methods are gone — the 6 call sites now call `write_load_file` /
    `write_tick_file` directly, which also removed the last 2 `# type: ignore[arg-type]`.
  - `ammo/casing/grenades/others/rpg7/weapons.py` merged into `database/items.py` (293 lines).
    `_template.py`, the unreachable `export_all_definitions_to_json` tail, and the 1.4 MB tracked
    `definitions_debug.json` deleted. `camo.py` kept — it is an image pipeline, not a table.
  - Real de-duplication found on the way: `ammo.py` re-implemented `load_model()` inline, and the
    14 perk machines were 14 hand-written `Item(...)` lines → one `PERK_MACHINES` table.
  - ⚠ **Registration order is load-bearing** and nearly broke this: my first draft split the perk
    machines into a "single dye" loop and a "two-tone" loop, which reorders `Mem.definitions` and
    would have moved every downstream artefact (loot tables, item models, lang keys). Merged back
    into one ordered table. `mystery_box.py` also imported `WEAPON_STATS` from the deleted
    `database.weapons` — repointed to `database.items`.
  - `MultiplayerMode` / `ZombiesMode` / `MissionsMode` converted back to plain `generate_*()`
    functions (requested at review after I initially proposed dropping this). `GameMode` and
    `generator.py` deleted; `McfunctionGenerator` folded into `GameModeVariant`, which is the only
    remaining user; the two spawn-marker macros moved to `core/spawning.py` as free functions.
  - The ~2 400-line dedent was done with a token-aware one-shot script, not a regex. **PEP 701 is
    the trap:** an f-string replacement field can contain lines of Python code (see the
    `late_join_flow_lines(...)` call inside `zombies/join_game`), and the same file mixes those with
    mcfunction body lines that must not move. The script protects every `FSTRING_START..FSTRING_END`
    span wholesale — leaving replacement-field code slightly over-indented is harmless, changing an
    emitted byte is not. Output byte-identical, so the protection held.
  - Final P3: **99 → 91 Python files, −240 LOC.**
- **2026-07-24** — **P4 done (awaiting review).** 97 `_zoom` source models became `parent:` children.
  **Resource pack 173.7 MB → 103.8 MB (−69.9 MB, −40 %)**; source models 32.2 → 18.3 MB.
  485 models changed (97 × 5 camo variants), 0 files added or removed, datapack untouched.
  - **Equivalence proof:** a script resolves each new model's `parent` chain using vanilla merge
    rules (per-slot `display` override, `textures` merge, `elements` replace) and deep-compares to
    the baseline. **485/485 resolve identically.** This is the check to re-run if these models are
    ever touched again.
  - Two things the naive version would have broken, both found before building:
    1. **camo.py rewrites `override_model["textures"]` per material.** A `parent:`-only child has no
       textures, so every camo'd zoom model would silently have rendered *un-camo'd*. Fixed by
       retargeting the parent instead (`mgs:item/ak47` → `mgs:item/ak47_gold`) and skipping the
       blend — which is also why the saving is 5× the source saving.
    2. **StewBeet's `item_models` plugin injected a default `layer0` texture** named after the item,
       so `rpg7_zoom` demanded a non-existent `rpg7_zoom.png` and the build failed. Fixed upstream:
       a model that declares `parent` and no `textures` is a child and inherits them.
  - The 5 real exceptions (`mac10_zoom`, `spas12_zoom`, `vz61_zoom`, `g3a3_1_zoom`, `g3a3_3_zoom`)
    keep full standalone models — they differ in `elements`/`textures`, not just `display`.
  - **Renderer confirmation:** deleting `iso_renders/` and rebuilding regenerated all **632 renders
    byte-identically** (git-tracked, so `git status iso_renders` proves it) — an independent check
    through a real model renderer covering every camo variant. Also **0 dangling parent references**
    across the 499 models that now use an `mgs:` parent.
  - The client-side worry is settled by the pack itself: the **14 perk machines have always been
    `parent:`-only children with no `elements`** (`perk_machine_juggernog` = `{parent, textures}`),
    and they render in game today. The new zoom children are the same shape.
- **2026-07-24** — **P5a done (awaiting review).** **1510 → 1479 mcfunctions (−31)**, −51 command
  lines, −31 Python LOC. Output diff verified by re-deriving it: a script expands each baseline
  caller by hand and compares to the new build — **82/82 changed files match exactly**.
  - The 26 `zombies/feedback/sound_*` one-liners became a `zb_sound(name)` table inlined at 63 call
    sites. Removes a function dispatch per cue, so this is marginally *faster*, not slower.
    The two 2-command cues (`box_spin`, `box_spin_short`) were split into single commands so every
    table entry is exactly one command and guarded call sites inline safely.
  - ⚠ **Layering:** `core/weapon_drop.py` needed a cue, and importing it from `zombies/` created a
    circular import (`core → zombies → core`). The table moved to **`core/feedback.py`** — zombies
    already depends on core, never the reverse.
  - ⚠ **Plan correction:** `shared/maps/call_*_script_at_base` was filed under D1 (inlining), but
    they are **5-command** wrappers with 14 call sites — inlining would have *created* ~60 lines of
    duplication. Converted to one `$(script)` macro instead (6 → 1). Belongs in D2, not D1.
    Lesson for P5b: check the command count and call-site count before inlining anything.
- **2026-07-24** — **P5b analysed, not started. Recommend deferring it below P6.** No source
  changed; the finding is the deliverable.
  - ⛔ **`return run function X` makes a 2-command X non-inlinable.** `return run` takes exactly one
    command and returns, so `execute unless <cond> run return run function .../deny_x` cannot become
    `execute unless <cond> run return run tellraw …` — the second command (the deny sound) would
    **silently never fire**. A byte-diff would look plausible; only playing the game would reveal it.
  - This kills the whole `deny_*` family, which looked like the ideal P5b target: 25 of the 34 are
    exactly `tellraw` + deny sound with one caller, but **all 44 deny call sites are guarded and
    nearly all use `return run`**. Not inlinable at all.
  - Re-running the census with the correct rule (inlinable = single caller, no macro args, and
    `return run` only when the body is 1 command): **142 → 108 candidates**, 29 blocked by exactly
    this constraint. Of the 108: 24 bare calls, 73 guarded, 11 single-command behind `return run`.
  - **Recommendation:** do **P6 (D2) first.** P5b is 108 scattered hand edits across ~20 files for
    −108 files; P6 is ~15 loop-driven generators for −160 files — an order of magnitude better
    value per edit, and each one is a single localised change (e.g. `mystery_box/default_give`
    32 → 1, `pap/apply_field` 28 → 1, `admin/powerup_*` 11 → 1).
  - The `deny_*` family should instead go to **D5** (one shared `zombies/deny/*` taking the message
    via storage), which keeps a function to call and so survives `return run`.
- **2026-07-24** — **P6a done (awaiting review).** **1479 → 1384 mcfunctions (−95)**, −306 command
  lines. Only **5 files have real command-body changes** — the 5 dispatchers rewritten on purpose;
  the other 34 changed files differ in header comments only.
  - `mystery_box/default_give/*` **32 → 2.** The pool entry already carries `weapon_id`/
    `magazine_id`/`mag_count`/`consumable`, and `mystery_box.result` holds the chosen entry, so one
    shared `default_give/weapon` reads them back instead of 31 functions restating literals.
    Verified field-by-field against every removed function. `give_function` stays a per-map hook and
    monkey_bomb keeps its own (different flow).
    **Bonus:** this exposed `default_give/m1911` as dead code — `M1911` has `WEIGHT: 0` so it is
    excluded from the pool, yet a give function was still generated for it (`@within ???`).
  - `pap/apply_field/*` **28 → 1 macro** (`$(field)`). Cold path (PaP purchase), arg set is the
    fixed `STATS_FIELDS`, so each variant compiles once. Verified: all 28 removed bodies reproduce
    exactly under `$(field)` substitution, and all 28 dispatch lines rewrote consistently.
  - `wunderfizz/set_model/*` + `grant/*` **28 → 0**, no macro. Both were dispatched by a score index,
    so the 1-command model setter inlines straight into the two dispatch tables, and `grant`'s
    3 commands become "dispatch sets `perk_id`, then apply once". The apply is guarded on
    `perk_id` being set, preserving the original no-op for an out-of-range pick.
  - `zombies/admin/powerup_*` **11 → 1 macro** (`$(type)`); the dialog buttons pass the type.
- **2026-07-24** — **P6b done (awaiting review).** **1384 → 1349 mcfunctions (−35)**, −237 command
  lines, −45 Python LOC. 4 files added, 39 deleted, 15 modified (5 of those header-only).
  - `perks/pool/try_index/*` **14 → 1 macro** (`$(perk_id)`). The per-perk index constant is simply
    `#pool_roll` (the dispatcher only ever calls a perk at its own index), so it becomes a
    `scoreboard players operation`. Cold path: random-perk power-up and Wunderfizz use.
  - `perks/pool/count` **deleted** (−1 file, −71 commands). It walked all 14 perks with the same
    availability test `try_index` runs, purely so `choose` could early-return "none available".
    `choose_iter` already caps at one full loop and leaves `#pool_chosen` at −1, which is what both
    callers actually read — so the count was redundant work, not a guard.
  - `powerups/spawn_type/*` **11 → 1 macro.** `do_spawn_random` (dispatching on the shuffle-bag
    `type_num`) now just names the type and hands over to `spawn_display` (dispatching on the type
    string), so the per-type payload lives in **one** table instead of two parallel ones.
    The floating label is passed as a **quoted** text component and substituted raw, so the emitted
    `text:` is byte-identical to the 11 removed functions.
    - Gotcha worth remembering: the macro argument is named `label`, not `text`. `auto.lang_file`'s
      `TEXT_RE` matches any `text:"…"` textually, so with `text:'{"text":"Nuke",…}'` it translated
      the **outer** quoted value and produced 11 junk keys like
      `mgs.text_nukecolor_redbold_true`. Renaming the argument makes the inner component the
      leftmost match again; `en_us.json` is unchanged.
  - `mob/default/level_*` **5 → 0.** The versioned `level_N` was a one-line hop that the
    unversioned public `mgs:mob/default/level_N` already pinned to a version, so the public
    function now calls `on_new` directly.
    - This exposed a real bug: the map editor's enemy `function` field **suggested**
      `mgs:v5.1.0/mob/default/level_1`, contradicting the rule stated three functions above it
      ("saved enemy functions must not embed the pack version") and matching neither of the two
      other places that write that default. Fixed to `mgs:mob/default/level_1`.
  - `maps/editor/set_door_link_*` **8 → 2.** One entry point for the string fields and one for the
    numeric fields — a macro cannot re-quote its own argument, so `value:"$(value)"` and
    `value:$(value)` have to stay separate. The field name rides along as a second argument, and the
    suggested command still ends in the value, so editing it in chat is unchanged.

  **Dropped from P6b, with reasons** (all four were on the plan's estimate of −60):
  - `perks/apply/*` (14) — each is an arbitrary effect plus a **static** `tellraw`. Parameterising
    the message would turn the translate components into macro text, and `auto.lang_file` only
    lifts English out of literals, so the pack would silently lose 14 translation keys.
  - `perks/reapply/*` (10) — bodies are already the deduplicated `commands` lists. Inlining them
    would duplicate all 10 across **two** call sites (tombstone recovery and Who's Who revive).
  - `revive/hud_*` (4) and `mystery_box/hud_*` (5) — both are **warm** paths (downed-player tick,
    hover tick) and both are 2-command `return run` targets, so collapsing them needs either a
    per-tick macro or replacing the early returns with unconditional `unless data` guards on
    globally shared storage. −9 files is not worth either.
  - `zombies/types/*` (5) — not a duplication family at all; `normal`/`dog` are long and genuinely
    different, and the other three already delegate to `normal`. The plan mis-filed them.
- **2026-07-24** — **P7 done (awaiting review).** **1349 → 1320 mcfunctions (−29)**, −58 command
  lines, −93 Python LOC. D5 came in at more than twice its estimate; **D6 was dropped**.
  - **D5 turned out to be one family, not five.** Almost every `deny_*` in zombies is exactly
    `tellraw @s [MGS_TAG, <component>]` + the deny `playsound`. So the split is not
    "not_enough_points vs requires_power vs moving vs …" — it is **static message** (23 files) vs
    **message with a live price** (7 files):
    - `zombies/deny/message` takes the whole text component as a macro argument. The English stays
      a literal at each call site, so every translation key is preserved. Argument named `msg`, not
      `text`, for the lang_file reason recorded under P6b.
    - `zombies/deny/not_enough_points` takes `score` + `obj`. Mystery Box was the reason `obj` is an
      argument at all — its price lives in `mgs.config`, not `mgs.data`, which is why it never used
      the shared `deny_not_enough_points_body` helper.
    - Both are **one command at the call site**, so they survive the `return run` constraint that
      killed P5b's inlining idea. That is the whole point of routing through a function instead of
      inlining the two commands.
  - The plan claimed `deny_moving`/`deny_all_owned`/`deny_not_your_result`/`deny_in_use` "appear
    twice (mystery box + wunderfizz)" and could be shared. **They are not duplicates** — each pair
    says something different ("The Mystery Box is moving..." vs "Der Wunderfizz is moving..."). They
    collapse anyway, but as *callers of one handler*, not as one shared body.
  - `zombies/pap/deny_max_level` **deleted as dead code** — `@within ???`, no caller anywhere in the
    generated tree. Its key `mgs.this_weapon_is_already_at_max_pack_a_punch_level` leaves `en_us.json`.
  - Two files keep their own function because their bodies are 3 commands, not 2:
    `mystery_box/deny_pool_empty` (clears the stale result first) and `wallbuys/deny_hold_valid_slot`
    (picks its wording on Mule Kick). `pap/deny_not_enough_points_scope` also stays: its text
    contains an apostrophe, and a single-quoted SNBT argument would need `\'`, which lang_file would
    then extract *with* the backslash and mint a different key.
  - **Accepted lang diff:** `mgs.der_wunderfizz_is_moving` and `..._2` swapped values. Two distinct
    strings ("...moving..." and "...moving!") share a base key, and lang_file suffixes whichever it
    scans second; moving the deny text from `wunderfizz/deny_moving` into `wunderfizz/on_right_click`
    reorders them alphabetically. **Only `en_us.json` ships**, and both keys still map to their own
    correct English, so nothing renders differently in game.

  **D6 dropped.** The plan said `maps/editor/{create,list,save_lists,give_tools,summon_existing}/
  {multiplayer,zombies,missions}` were "measured near-identical". They are not:
  `save_lists/zombies` clears 12 element lists, `save_lists/missions` clears 6, and they name
  different storage paths; `give_tools` hands out a different toolbar per mode. They already come
  from **one** `for mode_key, mode_info in EDITOR_MODES.items()` loop over a shared table, so there
  is no Python duplication to remove either — the output differs because the modes differ.
  Collapsing them would mean driving the editor off a runtime element table: a much larger change
  than "−10 files, low risk", and one that buys nothing on the Python side.
  `players/row_{mode}` is the same story (multiplayer has team buttons, the others do not, and the
  tooltips are per-mode keys). Only `players/list_{mode}` is genuinely parameterisable, for −2.
