# Refactor audit

Measured on `main` at `694ac6c0`; `main` then moved to `147cee09` (StewBeet `>=3.9.4`, 9 more ruff rule families): a StewBeet 3.9.4 build gives the same datapack and resource pack text, and ruff numbers below use the new rules. Every number comes from a command listed in its section. Scripts live in `.refactor/audit/` (ignored by git). "HEAD build" means the committed `build/` exported with `git archive HEAD build | tar -x -C .refactor/head` (text files only), so numbers describe what the author's machine produced.

## 1. Build

| Item | Value |
|---|---|
| Generator | StewBeet 3.9.0 on beet 0.119, mecha 0.106 (installed, not in the pipeline), `beet.yml` pipeline of 24 plugins, user code `src.setup_definitions` (items) and `src.link` (everything else) |
| Source of truth | `src/` (332 `.py`, 291 Blockbench `.json` models), `assets/` (564 textures, 406 sounds), `beet.yml` |
| Output | `build/datapack`, `build/resource_pack`, 3 zips (4 when libraries download), `all_items.png`, `sha1_hashes.json` |
| Setup | `uv sync` (needs uv >= 0.9 to fetch Python 3.14: the image's uv 0.8.17 cannot; `pip install -U uv` gave 0.12.21). Rewrites `uv.lock` (+87 lines), reverted |
| Build command | `.venv/bin/stewbeet` |
| Duration | 32.5 s wall (`time`), StewBeet reports 26.9 s; `archive` alone 9.2 s |
| Determinism | `diff -rq` of a fresh build against the HEAD build: datapack identical except `load/check_dependencies` and `load/valid_dependencies` |
| Build is tracked in git | 7,460 files under `build/`, zips included (3.2 MB datapack, 33 MB resource pack each) |

Environment effects seen in this container (not bugs of the project, but they shape the safety net):

| Effect | Cause | Consequence |
|---|---|---|
| Libraries not downloaded | `api.modrinth.com`, `api.smithed.dev` answer 403 through the proxy | `check_dependencies` loses 41 lines, `valid_dependencies` and `en_us.json` (13 keys) change, `MCGunsSystem_datapack_with_libs.zip` is deleted |
| `D:/latest_snapshot/world/datapacks/livereload/` created at the repo root | `livereload` plugin with the Windows path of `beet.yml`, relative on Linux | removed by hand after each build |
| 312 binary files (223 `.ogg`, 89 `.png`) show as typechange | committed with mode 120000 (symlink) and the file content as link target (`git ls-files -s build \| awk '$1=="120000"'`) | a Linux checkout makes them broken links; any build makes them regular files |

## 2. Volume

Commands: `.venv/bin/python .refactor/audit/volume.py .refactor/head/build` (writes `.refactor/audit/out/volume.md`), `git ls-files`.

### Source (tracked)

| Folder | Files | Lines | Blank | Comment | Docstring |
|---|---:|---:|---:|---:|---:|
| `src/*.py` | 2 | 296 | 43 | 16 | 25 |
| `src/config` | 23 | 2,518 | 156 | 90 | 221 |
| `src/database` (.py) | 2 | 570 | 75 | 36 | 54 |
| `src/functional/*.py` | 4 | 927 | 118 | 213 | 43 |
| `src/functional/core` | 12 | 1,051 | 186 | 149 | 86 |
| `src/functional/helpers` | 9 | 803 | 121 | 62 | 228 |
| `src/functional/main` | 5 | 448 | 65 | 92 | 5 |
| `src/functional/map_editor` | 17 | 2,164 | 386 | 350 | 77 |
| `src/functional/missions` | 12 | 780 | 179 | 179 | 49 |
| `src/functional/multiplayer` | 60 | 6,423 | 1,127 | 1,223 | 381 |
| `src/functional/progression` | 13 | 2,158 | 274 | 127 | 747 |
| `src/functional/shaders` | 6 | 1,207 | 214 | 89 | 121 |
| `src/functional/weapon` | 39 | 4,100 | 788 | 948 | 106 |
| `src/functional/zombies` | 128 | 12,715 | 2,313 | 2,723 | 508 |
| **Python total** | **332** | **36,160** | **6,045** | **6,297** | **2,651** |
| `src/database/models/*.json` (Blockbench) | 291 | 884,864 | | | |

"Comment" counts every line starting with `#`, so it includes the 3,717 mcfunction comment lines written inside generator strings (section 6). "Docstring" counts statement-position string literals (`ast`).

Other tracked text: `README.md` 187 lines, `TODO_26.3_SHADERS.md` 92, `specs/` 23 `.md` / 3,530 lines, `.claude/skills` 10 `.md` / 2,476, `.specify` 6 `.md` + 6 `.ps1` + 7 config / 2,302, `scripts/verify.py` 238, `assets/*.py` 7 / 380, `upload.py` 58, `weapon_list.txt` 45, `beet.yml` 132, `pyproject.toml` 70. Untouchable originals: `based_of/` 1,571 files, `iso_renders/` 651 PNG, `assets/` 975 media files. `.git` is 342 MB.

### Output (HEAD build)

| Datapack registry | Files | Lines | Bytes |
|---|---:|---:|---:|
| `function` (.mcfunction) | 1,617 | 38,836 | 13,996,189 |
| `function` (.mcfunction.map, sniffer source maps, shipped in the zip) | 1,607 | 16,175 | 452,610 |
| `loot_table` | 632 | 139,268 | 5,447,301 |
| `advancement` | 188 | 6,637 | 117,186 |
| `dialog` | 23 | 577 | 39,122 |
| `tags/block` | 25 | 619 | 16,078 |
| `tags/function` | 44 | 204 | 2,839 |
| `predicate` | 27 | 254 | 4,035 |
| `item_modifier` | 14 | 157 | 2,438 |
| `enchantment`, `damage_type`, other tags | 6 | 56 | 793 |

| .mcfunction lines | Count |
|---|---:|
| Total | 38,836 |
| Commands | 15,435 |
| Macro lines (`$`) | 861 |
| Comments | 15,602, of which 11,526 are StewBeet `auto.headers` (`#>`, `# @within`) and 4,076 come from the generator |
| Blank | 7,799 |

| Resource pack folder | Files | JSON lines | Bytes |
|---|---:|---:|---:|
| `assets/mgs/models` | 1,161 | 3,888,647 | 76,834,754 |
| `assets/mgs/items` | 1,161 | 6,966 | 100,716 |
| `assets/mgs/post_effect` | 49 | 2,610 | 61,791 |
| `assets/minecraft/lang` | 1 | 1,386 | 73,408 |
| `assets/mgs/sounds.json` | 1 | 1,130 | 33,176 |
| fonts, shaders, overlays | 17 | 460 | 32,580 |

### Total commands and per-tick commands

| Measure | Value | Command |
|---|---:|---|
| Command lines generated | 15,435 | `volume.py` |
| Functions reachable from `#minecraft:tick` (calls only, static upper bound) | 990 / 1,617 | `.refactor/audit/tick.py .refactor/head/build/datapack` |
| Command lines in those functions | 7,930 | same |
| Run every tick whatever the game state (calls without `if`/`unless`) | `tick` 24 lines; per player: `player/tick` 49 + `zoom/main` 10 + crosshair 19 + `utils/copy_gun_data` 6 + `switch/main` 5 + `switch/check_fire_mode_on_drop` 2 = 91 lines; per grenade: 24 | same, early `return`s make the real count lower |
| Advancement criteria evaluated every tick per player | 180 (`minecraft:tick` trigger: zb 100, mp 56, mi 23, root 1) | `json` scan of `advancement/` |
| Commands run on every `/reload` | 1,677 in 9 functions, 7.85 MB of mcfunction | load closure in `tick.py` |

### Top 30 source files (Python lines)

| # | File | Lines |
|---:|---|---:|
| 1 | `src/functional/map_editor/summon.py` | 304 |
| 2 | `src/config/catalogs.py` | 304 |
| 3 | `src/functional/map_editor/save.py` | 303 |
| 4 | `src/functional/zombies/maps.py` | 300 |
| 5 | `src/functional/multiplayer/loadouts/class_selection.py` | 296 |
| 6 | `src/functional/weapon/common.py` | 293 |
| 7 | `src/functional/zombies/machines/perks/definitions.py` | 290 |
| 8 | `src/functional/zombies/game/round/spawning.py` | 289 |
| 9 | `src/database/items.py` | 289 |
| 10 | `src/functional/player_config.py` | 287 |
| 11 | `src/database/camo.py` | 281 |
| 12 | `src/functional/multiplayer/loadouts/editor/save.py` | 279 |
| 13 | `src/functional/zombies/objects/doors.py` | 273 |
| 14 | `src/functional/progression/advancements/catalog/zombies.py` | 270 |
| 15 | `src/functional/progression/curve.py` | 269 |
| 16 | `src/functional/map_editor/zb_config.py` | 268 |
| 17 | `src/functional/multiplayer/loadouts/browsing/my_loadouts.py` | 265 |
| 18 | `src/functional/mob_ai.py` | 264 |
| 19 | `src/functional/weapon/firing/raycast/hits.py` | 263 |
| 20 | `src/functional/shaders/hurt.py` | 262 |
| 21 | `src/functional/multiplayer/gamemodes/domination.py` | 259 |
| 22 | `src/functional/core/weapon_drop.py` | 259 |
| 23 | `src/functional/shaders/flash.py` | 257 |
| 24 | `src/config/stats/weapons/pistols.py` | 256 |
| 25 | `src/functional/weapon/firing/sound.py` | 255 |
| 26 | `src/functional/weapon/firing/casing.py` | 254 |
| 27 | `src/functional/weapon/ammo/switch.py` | 248 |
| 28 | `src/functional/zombies/machines/pap/anim.py` | 244 |
| 29 | `src/functional/map_editor/handlers.py` | 243 |
| 30 | `src/setup_definitions.py` | 242 |

### Top 30 output files

By lines, the 30 largest output files are all camo copies of gun models (`models/item/m249_3_*.json` 12,889 lines each, then `m249_1_*` 11,792, `m249_2_*` 11,733, `m249_*` 10,460, `svd_4_*` 9,804, `fnfal_4_*` 9,738). By commands:

| # | Function (`mgs:v5.1.0/` unless noted) | Commands | Lines |
|---:|---|---:|---:|
| 1 | `load/set_items_storage` (7.76 MB) | 1,163 | 1,171 |
| 2 | `load/confirm_load` | 412 | 699 |
| 3 | `zombies/stop` | 158 | 212 |
| 4 | `zombies/start` | 157 | 244 |
| 5 | `multiplayer/editor/save` | 114 | 178 |
| 6 | `maps/editor/show_element_config` | 99 | 108 |
| 7 | `multiplayer/refresh_sidebar_ffa` | 94 | 130 |
| 8 | `zombies/game_tick` | 87 | 215 |
| 9 | `multiplayer/start` | 86 | 174 |
| 10 | `maps/editor/handle_zb_defaults` | 68 | 89 |
| 11 | `zombies/pap/on_right_click` | 67 | 134 |
| 12 | `player/config/process` | 66 | 126 |
| 13 | `maps/editor/process_element` | 65 | 107 |
| 14 | `zombies/perks/setup_iter` | 61 | 100 |
| 15 | `zombies/pap/compute_max_level` | 61 | 71 |
| 16 | `maps/editor/handle_zb_object` | 61 | 96 |
| 17 | `projectile/damage_entity` | 55 | 114 |
| 18 | `zombies/whos_who/revive_complete` | 54 | 69 |
| 19 | `weapon/hit_direction` | 53 | 72 |
| 20 | `maps/editor/backfill_zb_defaults` | 52 | 61 |
| 21 | `zombies/inventory/enforce_slot` | 50 | 80 |
| 22 | `ammo/inventory/find` | 50 | 68 |
| 23 | `zombies/perks/tombstone_collect` | 49 | 70 |
| 24 | `projectile/explode` | 49 | 99 |
| 25 | `player/tick` | 49 | 125 |
| 26 | `multiplayer/my_loadouts/manage_prep` | 48 | 57 |
| 27 | `load/valid_dependencies` | 48 | 63 |
| 28 | `lore/compute_values` | 47 | 75 |
| 29 | `mgs:zombies/bonus/max_ammo` | 46 | 64 |
| 30 | `zombies/traps/setup_iter` | 46 | 76 |

## 3. Call graph and dead code

Commands: `.refactor/audit/reach.py` (reachability), `.refactor/audit/ids.py` (objectives, storages, tags), `.refactor/audit/dangling.py` (0 dangling references today). Entry points: `#minecraft:load`, `#minecraft:tick`, every advancement, every `minecraft:` tag, `#common_signals:signals/on_new_item`, the 11 non-versioned `mgs:` functions, the `mgs:i/*` loot tables (README API). Edges: every id token found in a command or JSON (calls, `schedule`, macro patterns such as `zombies/perks/apply/$(perk_id)`, function ids passed as data, dialog `run_command`, enchantment `run_function`, advancement rewards, tag values). StewBeet's own headers mark the same functions `@within ???`.

### Unreachable functions: 37 of 1,617, 240 commands

| Function (`mgs:v5.1.0/`) | Cmds | Generated at | Finding |
|---|---:|---|---|
| `dialogs/config/{global,personal,damage_debug,grenade_power,rpg_power,infinite_ammo,instant_kill,max_ammo,quick_reload,quick_swap}`, `dialogs/multiplayer/setup/{gamemode,score_limit,time_limit}`, `dialogs/zombies/{admin,admin/powerups,setup/variant}` | 16 | `helpers/dialogs.py:81` (`wrapper` defaults to True) | dead: the 16 dialogs are reached through `show_dialog` actions; 4 other wrappers are called |
| `maps/multiplayer/store_loaded_idx` | 1 | `multiplayer/maps.py:38` | dead |
| `zombies/inventory/recreate_critical_items` | 5 | `zombies/player/inventory/hooks.py:87` | dead |
| `zombies/pap/refill_matching_magazines` | 42 | `zombies/machines/pap/magazines.py:64` | dead, `pap_upgrade_magazines` is the one called |
| `zombies/pap/set_item_name` | 1 | `zombies/machines/pap/lore.py:172` | dead, `set_item_name_with_level` is the one called |
| `zombies/wallbuys/count_guns` | 4 | `zombies/objects/wallbuys/give.py:59` | dead |
| `zombies/wallbuys/lookup_magazine_id` | 31 | `zombies/objects/wallbuys/give.py:29` | dead, same shape as the called `shared/drops/mag_lookup` |
| `zombies/wallbuys/render_hover_title` | 2 | `zombies/objects/wallbuys/hover.py:27` | dead |
| `utils/update_all_lore` + `lore/{extract_stats,compute_values,build_gun,build_grenade,append_*,apply}` (10) | 132 | `weapon/ammo/lore/` (352 Python lines) | never called; also writes 13 `mgs:lore_templates` keys on every load. README sells "Runtime lore rebuilding from weapon stats" |
| `maps/multiplayer/default_maps` | 2 | `multiplayer/maps.py:20` | only member of `#mgs:maps/register`, a tag nothing calls: the Hijacked and Highrise maps are never registered |
| `maps/multiplayer/register_map` | 1 | `multiplayer/maps.py:29` | registration helper with no caller |
| `zombies/on_round_start` | 1 | `zombies/objects/barricades/hooks.py:36` | meant for `#mgs:zombies/on_round_start` (empty): the 25-repairs-per-round cap on barricade points never resets until the game stops |
| `progression/recompute_all` | 2 | `progression/__init__.py:90` | "Admin entry point" per its comment, documented nowhere |

### Other unreferenced resources

| Resource | Size | Note |
|---|---:|---|
| loot table `mgs:zombies/powerup_drop` | 5 lines | dead |
| loot table `mgs:creative_loot_table` | 632 lines | StewBeet convention, nothing in the pack reads it |
| predicate `mgs:v5.1.0/input/any` | 9 lines | dead (`zombies/player/revive/setup.py:27`) |
| block tags `v5.1.0/{air,fence_gate,activate,jump,sounds/special_sound}` | 100 lines | dead (`fence_gate` is only listed by `air`) |
| function tag `#mgs:maps/register` | | no caller (see `default_maps`) |
| storage `mgs:items all` | 1,163 writes, 7.76 MB | StewBeet `datapack.loading` writes every item on every load; nothing in the pack reads it |
| functions with no command | 11 | `maps/multiplayer/hijacked/{start,tick,join,leave,respawn}`, `maps/zombies/kino_der_toten/{join,respawn}`, `multiplayer/gamemodes/{ffa,tdm}/cleanup`, `tdm/tick`, `zombies/prep_tick` (called every tick while preparing) |
| function tags with 0 values but callers | 21 | API hooks for other packs (`#mgs:signals/*`, `#mgs:zombies/*`, ...), kept |

### Scoreboard objectives: 296 created, 12 never read

| Objective | Writes | Note |
|---|---:|---|
| `mgs.mi.timer`, `mgs.mi.total_enemies`, `mgs.mp.gm_timer`, `mgs.mp.timer`, `mgs.player` | 0 | created only |
| `mgs.zoom_timer` | 4 | incremented every tick per aiming player (`zoom/main`), never read |
| `mgs.switch_cooldown`, `mgs.mp.edit_step`, `mgs.zb.tsp.tombstone`, `mgs.zb.wwp.whos_who` | 1 to 3 | write-only |
| `mgs.special.additional_shots` | 5 | Double Tap sets it, no shot reads it: the perk sold for 2000 points ("Fires an extra bullet with every shot") has no effect |
| `mgs.special.juggernaut` | 3 | multiplayer Juggernaut perk flag, no effect anywhere |

Storage keys written and never read (33) are mostly library inputs (`bs:in`, `smithed.actionbar:input`), signal payloads for listeners (`mgs:signals`), `mgs:items all`, and 20 `mgs:temp` scratch keys to check one by one. Entity tags added and never tested in a selector: `mgs.casing`, `mgs.door_front`, `mgs.dying_wish_active`, `mgs.guardian_golem`, `mgs.mb_base`, `mgs.perk_machine`, `mgs.trap_base`, `mgs.wallbuy`, `mgs.wallbuy_display`, `bs.entity.interaction` (also in the `specs/README.md` inbox).

## 4. Duplication

Command: `.refactor/audit/dup.py .refactor/head/build/datapack` (masks ids, numbers, strings and objective names, then groups identical shapes), plus the model scan below.

| Group | Members | Size | What varies |
|---|---:|---:|---|
| Camo copies of gun models, `models/item/<gun>_<camo>.json` | 444 | 2,831,600 lines, 56.5 MB | only `textures`; the 408 zoom variants already use `parent` |
| Challenge reward functions `progression/adv/{mi,mp,zb}/*/reward_N` | 133 | 11 commands each, 1,463 | title key, description key, XP, branch, chain, tier |
| Level reward functions `progression/adv/*/level/reward_N` | 30 | 11 each, 330 | same |
| Recoil kick functions `kicks/type_N[_ds]` | 12 | 10 each, 120 | numbers (hot path: per shot) |
| Award functions `progression/{mp,zb}/award_*` | 28 | 3 to 5 each, 115 | XP amount, message key; 17 are exact copies of another |
| Slot loops unrolled per inventory slot (`ammo/inventory/find`, `has_ammo`, `ammo/reserve/scan`, `zombies/pap/pap_upgrade_magazines`, `refill_matching_magazines`, `max_ammo`, `max_ammo_reload_weapons`, `shared/drops/give_mag`, `scavenger_refill`, `ammo/update_old_weapon`, `zombies/inventory/enforce_slot`) | 11 | 27 slot lines each, about 300 | slot name |
| Other unrolled lists (78 functions with one line shape repeated 8+ times) | 78 | 1,691 lines | ids, slots, perks |
| Exact duplicate bodies | 30 functions in 13 groups | 17 redundant | none |
| Item loot tables `mgs:i/*` | 628 | 138,620 lines | StewBeet item system: one table per item and camo |
| `load/set_items_storage` | 1 | 7.76 MB | every item again, as SNBT |
| Advancements in 18 shape families | 175 / 188 | 6,299 lines | ids, keys, thresholds |
| Python source (`npx jscpd@4 ./src --ignore "**/*.json"`, the repo CI) | 2 clones | 64 lines (0.18 %) | |

The duplication is in the output, not in the Python: the generator writes these from loops and tables.

## 5. Performance (static)

No profiler can run here (section 9), so this is a static count. Command: `.refactor/audit/tick.py`.

| Hotspot | Where | Cost per tick |
|---|---|---|
| 180 `minecraft:tick` criteria on the challenge advancements | `advancement/challenges/**` | up to 180 `entity_scores` checks per player per tick until earned; the 14 `mgs.adv.*` scores change at 18 call sites only |
| `execute as @e[tag=mgs.grenade]` with no `type=` and no gate | `tick` | full entity scan of every dimension every tick, also with no grenade in the world; the tag is only ever on `item_display` |
| `@e[tag=mgs.slow_bullet]` (only `item_display`), `@e[tag=mgs.armed]` (any mob) | `tick` | full scans, gated by counters |
| 254 `@e[tag=...]` selectors with neither `type=` nor `distance=` in the tick closure | top: `maps/editor/particles` 18, `zombies/game_tick` 12, `multiplayer/pick_spawn` 10 | each one scans all entities |
| 209 entity NBT reads in the tick closure | top: `projectile/explode` 13, `casing/calculate_vectors` 12, `grenade/detonate_frag` 10 | event paths, not idle |
| `mgs.zoom_timer` written twice per aiming player per tick | `zoom/main` | dead work |
| 4 calls to `stamina_tick` guards and 6 storage compound tests per player per tick | `player/tick` | small |
| 1,163-command, 7.76 MB item storage write on every `/reload` | `load/set_items_storage` (StewBeet) | load time and world size (storage is saved in `data/command_storage_mgs.dat`) |
| 513 macro lines in the tick closure; slot loops with 27 macro lines re-parsed per new argument set | `ammo/inventory/*`, `ammo/reserve/scan` | per reload or idle ammo scan |

## 6. Text written by the generator

Commands: `.refactor/audit/text.py`, `uvx --from stouputils@latest stouputils check src scripts assets upload.py README.md` (26.8.0; the locked 26.7.2 has no `check`), scans of the lang file and of the output.

| Measure | Value |
|---|---:|
| mcfunction comment lines written in generator strings | 3,717 |
| of which the heuristic (60 % of the comment's words in the next command) flags as paraphrase | 381 |
| Python comment lines (section banners excluded) | 1,917 |
| of which flagged as paraphrase | 148 |
| Decorative banners (box drawing, `===`) | 42 |
| Lines narrating a past state (`used to`, `no longer`, `legacy`, `the old`, `kept so`, ...) | 72 (grep, includes some false hits) |
| `stouputils check` violations | 1,040 in 206 files: banned characters 448 (em-dash 316, U+2192 rightwards arrow 103, U+2500 box drawing 24, U+2026 ellipsis 5), stranded-fragment 186, typed-argument 165, long-comment 133, final-newlines 33, examples-header 29, tab-indentation 22, long-docstring 11, constant-comment 6, space-alignment 4, split-span 2, module-docstring-position 1 |

Examples (file:line in `src/`): paraphrases `map_editor/handlers.py:64` `# Summon permanent marker` over `function .../summon_spawn_marker`, `map_editor/save.py:73` `# Write back to storage` over `function .../write_back`, `map_editor/enter.py:39` `# Load map data`; past narration `helpers/dialogs.py:47` ("Kept so existing ... still work; the function is now a one-liner"), `helpers/dialogs.py:69` ("unlike the inline SNBT form this replaces"), `player_config.py:243` ("Replaces the old clickable-chat menu"), `weapon/grenade/effects.py:61` ("used to drop the count to 0"); tuple rows `helpers/dialogs.py:105` `list[tuple[str, str, str, str]]`.

In-game text:

| Measure | Value |
|---|---:|
| `en_us.json` entries | 1,384 |
| entries with an em-dash (e.g. `mgs.no_map_selected_open_the_setup_menu_first`, `mgs.dying_wish_berserk`) | 25 |
| em-dashes in non-translated text (sidebars, `refresh_sidebar_demo`) | 17 |
| U+2550 (84) and U+2500 (24) box-drawing banners in `tellraw` (`missions/victory`, `zombies/game_over`, `snd/start_round`, `demo/start_round`) | 108 |
| U+25C0 left triangle (25, Back buttons) and U+25B6 right triangle (6) | 31 |
| `➤` in lore labels | 12,740, allowed (author's call); `stouputils check` does not flag U+27A4, only U+2192, so no stouputils change is needed |

Documentation versus code:

| Doc | Finding |
|---|---|
| `README.md` | "Runtime lore rebuilding from weapon stats" describes the unreachable lore pipeline; a French `<summary>` in the English page; "Exemple"; a design TODO (kill cam) duplicated by `specs/004`; Double Tap described in game as a working perk |
| `specs/README.md` | links `src/functional/zombies/README.md`, which does not exist; says 001 "Researched, nothing ported" (the post-effect migration is shipped) and 007 "nothing built" (188 advancements ship) |
| `.github/copilot-instructions.md` | "we are in 26.1 now" (26.3); points to `minecraft_source_code`, a submodule entry with no `.gitmodules` (empty checkout) |
| `upload.py` | a SimplEnergy summary from another project and 3 commented-out upload blocks (37 of 58 lines) |
| `weapon_list.txt` | a 3-item TODO list next to a weapon list nothing reads |

## 7. Python generator quality

| Check | Result | Command |
|---|---|---|
| ruff (project `pyproject.toml` of `147cee09`) | 1,885 findings: E501 1,877 (line > 135, nearly all mcfunction lines inside strings), FBT003 3, PERF401 2, RET505 2, SIM300 1 | `.venv/bin/ruff check src --statistics` |
| pyright strict | 0 errors | `.venv/bin/pyright src --pythonpath .venv/bin/python` (without `--pythonpath`: 3,607 errors cascading from unresolved imports) |
| complexipy (max 15) | 0 functions over | `uvx complexipy src --failed --max-complexity-allowed 15` |
| `Any` / `cast(` / `pyright: ignore` | 42 / 11 / 3 | grep |
| Tuple tables of 3+ fields | 14 annotations (`zombies/common.py` slots, `helpers/dialogs.py` options, `multiplayer/game/sidebar.py`, `database/camo.py` jobs, ...) | grep |
| Anonymous boolean parameters | 14 (`register_dialog(wrapper=True)`, `gm_dispatch(ret=False)`, ...) | grep |
| Files over 250 lines | 26 (max 304) | `wc -l` |
| `write_versioned_function` calls | 1,252 | grep |

## 8. Frozen identifiers

Renaming any of these needs a migration and the author's approval.

| Kind | Count | Ids |
|---|---:|---|
| Scoreboard objectives | 296 | listed below |
| Storages | 16 | `mgs:maps` {missions, multiplayer, zombies} (map definitions), `mgs:multiplayer` {classes_list, custom_loadouts, game, next_loadout_id, player_data, primary_slot_table, secondary_slot_table} (player loadouts), `mgs:zombies` {camo_variants, door_names, game, mystery_box, mystery_box_pool, mystery_box_weights, pap_anim_slot, pap_data, pap_pending_cosmetics, perk_data, scope_variants, tombstone_inv, wallbuy_data, ww_inv}, `mgs:missions` {game}, `mgs:config` {no_magazine}, `mgs:data` {_pu_queue}, `mgs:items` {all}, `mgs:lore_templates` (13 keys), `mgs:signals` (12 payload keys, API), `mgs:gun`, `mgs:input`, `mgs:temp` (262 scratch keys), `mgs:editor`, `bs:in`, `bs:out`, `smithed.actionbar:input` |
| Entity tags | 265 | listed below; `mgs.element.*` and `mgs.map_element` sit on map editor markers saved in worlds |
| Item identity | 628 items, 637 `mgs` custom_data keys | `custom_data.mgs.{gun,magazine,stats,sounds,<item_id>,...}`, `custom_data.smithed.{id,origin,ignore}`, item models `mgs:<id>`, enchantment `mgs:left_click` (on every gun), loot tables `mgs:i/<id>` (README API) |
| Advancements | 183 saved in player data | `mgs:challenges/**`, plus `mgs:v5.1.0/**` technical ones |
| Public functions | 11 | `mgs:_give_all`, `mgs:config`, `mgs:mob/default/level_{1..5}` (stored in map enemy entries), `mgs:zombies/bonus/{max_ammo,nuke}`, `mgs:zombies/recover` |
| Function tags (API) | 44 | `#mgs:signals/*`, `#mgs:maps/*_script`, `#mgs:{multiplayer,missions,zombies,progression}/*`, `#mgs:{load,dependencies,enumerate,resolve}`, `#common_signals:signals/on_new_item` |
| Scheduled functions (saved in level.dat while pending) | 11 | `load/valid_dependencies`, `{missions,multiplayer,zombies}/end_prep`, `{missions,zombies}/preload_complete`, `multiplayer/gamemodes/{demo,snd}/start_round`, `zombies/{bonus/nuke_loop,start_round,stop}` |
| Stored commands | map data | `start_commands`, `respawn_commands`, enemy `function`, base marker `start_function` / `tick_function` in `mgs:maps` |
| Bossbars / teams / stopwatch / trigger | 5 / 6 / 1 / 1 | `mgs:pu_{bonfire_sale,double_points,fire_sale,insta_kill,unlimited_ammo}` / `mgs.{blue,ffa,horde,mi_mobs,red,zombies}` / `mgs:clock` / `mgs.player.config` |
| Other | | dialogs `mgs:open_class_menu` and `minecraft:quick_actions` tag, damage type tags, `load.status` entries `#mgs.{major,minor,patch,loaded}` |

Objectives: load.status, mgs.ab_force, mgs.acoustics_level, mgs.adv.mi.completed, mgs.adv.mi.kills, mgs.adv.mp.headshots, mgs.adv.mp.kills, mgs.adv.mp.objectives, mgs.adv.mp.wins, mgs.adv.zb.best_round, mgs.adv.zb.box, mgs.adv.zb.headshots, mgs.adv.zb.kills, mgs.adv.zb.pap, mgs.adv.zb.perks, mgs.adv.zb.revives, mgs.adv.zb.spending, mgs.burst_count, mgs.class_menu, mgs.config, mgs.cooldown, mgs.cross_from, mgs.cross_to, mgs.data, mgs.demo_fuse, mgs.demo_owner, mgs.demo_prog, mgs.demo_state, mgs.dps, mgs.dps_timer, mgs.drop_timer, mgs.dropped, mgs.flash_id, mgs.flash_off, mgs.flash_slot, mgs.food, mgs.fx_deaths, mgs.grenade_launch, mgs.grenade_spin, mgs.health, mgs.held_click, mgs.hp_prev, mgs.hurt_fall_until, mgs.hurt_from, mgs.hurt_fx, mgs.hurt_out_until, mgs.hurt_pending, mgs.last_hit, mgs.last_muzzle_flash, mgs.last_selected, mgs.mb.anim, mgs.mb.box, mgs.mb.buyer, mgs.mb.pid, mgs.mb.timeslip, mgs.mb.willmove, mgs.mi.deaths, mgs.mi.died_here, mgs.mi.in_game, mgs.mi.kill_base, mgs.mi.kill_total, mgs.mi.kills, mgs.mi.timer, mgs.mi.total_enemies, mgs.mob.active_time, mgs.mob.sleep_time, mgs.mob.timer, mgs.mp.bphase, mgs.mp.bx, mgs.mp.by, mgs.mp.bz, mgs.mp.class, mgs.mp.death_count, mgs.mp.deaths, mgs.mp.default, mgs.mp.dom_owner, mgs.mp.dom_progress, mgs.mp.edit_points, mgs.mp.edit_step, mgs.mp.edit_target, mgs.mp.ffa_rank, mgs.mp.gm_timer, mgs.mp.in_game, mgs.mp.kills, mgs.mp.map_disp, mgs.mp.map_edit, mgs.mp.map_idx, mgs.mp.map_mode, mgs.mp.pid, mgs.mp.prev_class, mgs.mp.spectate_timer, mgs.mp.team, mgs.mp.timer, mgs.mp.xp_level, mgs.mp.xp_prog, mgs.mp.xp_session, mgs.mp.xp_total, mgs.pap_anim, mgs.pending_clicks, mgs.player, mgs.player.config, mgs.player.damage_debug, mgs.player.hitmarker, mgs.previous_dps, mgs.previous_selected, mgs.remaining_bullets, mgs.reserve_ammo, mgs.sidebar, mgs.special.{additional_shots, deadshot, double_points, electric_cherry, flak_jacket, infinite_ammo, instant_kill, juggernaut, overkill, phd_flopper, quick_fix, quick_reload, quick_swap, scavenger, tactical_mask, timeslip, tracker, widows_wine}, mgs.stam, mgs.stam_bonus, mgs.stam_dirty, mgs.stam_max, mgs.stam_out, mgs.stam_rest, mgs.stam_seen, mgs.stam_swim, mgs.stuck_id, mgs.switch_cooldown, mgs.total_kills, mgs.zb.ability, mgs.zb.ability_cd, mgs.zb.barricade.{bang_at, id, r_timer, radius, removing_id, rep_at, repairing_id, rp_timer, state}, mgs.zb.barricade_repairs, mgs.zb.bleed, mgs.zb.door.{anim, bgid, link, paid, partial, price, rot}, mgs.zb.downed, mgs.zb.downed_id, mgs.zb.downs, mgs.zb.dw_cd, mgs.zb.dw_timer, mgs.zb.dw_uses, mgs.zb.ec_last, mgs.zb.escort_ttl, mgs.zb.horde_cd, mgs.zb.in_game, mgs.zb.kills, mgs.zb.lethal_type, mgs.zb.pap.{id, power, price, timeslip}, mgs.zb.pap_mid, mgs.zb.pap_s, mgs.zb.passive, mgs.zb.perk.{base_price, id, partial, power, price} and mgs.zb.{perk, perkpaid, tsp, wwp}.{deadshot, double_tap, dying_wish, electric_cherry, juggernog, mule_kick, phd_flopper, quick_revive, speed_cola, stamin_up, timeslip, tombstone, whos_who, widows_wine}, mgs.zb.player_hit, mgs.zb.points, mgs.zb.prev_kills, mgs.zb.pu.timer, mgs.zb.pu.type, mgs.zb.qr_uses, mgs.zb.revive_p, mgs.zb.rise_tick, mgs.zb.sb_rank, mgs.zb.spawn.gid, mgs.zb.spawn.sid, mgs.zb.stuck_dist, mgs.zb.stuck_ticks, mgs.zb.stuck_x, mgs.zb.stuck_z, mgs.zb.trap.{cd, cd_max, dur, id, power, price, rx, ry, rz, timer, timeslip, type}, mgs.zb.ts.state, mgs.zb.ts.timer, mgs.zb.vox_attack, mgs.zb.vox_death, mgs.zb.vox_sprint, mgs.zb.wb.{id, price, rfpap, rfprice}, mgs.zb.wf.{allperks, anim, buyer, id, paid, perk, power, price, timeslip, willmove}, mgs.zb.wf_pid, mgs.zb.ww.id, mgs.zb.ww_last, mgs.zb.xp_level, mgs.zb.xp_prog, mgs.zb.xp_pts_prev, mgs.zb.xp_spent_acc, mgs.zb.xp_total, mgs.zb_sidebar, mgs.zoom, mgs.zoom_fx, mgs.zoom_fx_off, mgs.zoom_timer.

Entity tags: _pw_new, bs.entity.interaction, bs.raycast.omit, convention.debug, global.ignore, global.ignore.kill, mgs_name_probe, and `mgs.` + {_barricade_new_d, _ed_new_disp, _trap_new_bs, _trap_new_head, _trap_new_i, _trap_new_m, _turret_cand, _turret_target, _turret_visible, already_killed, armed, barricade_display, barricade_frozen, barricade_removing, barricade_repairing, casing, check_nearest, coord_stick_user, death_watch, demo_atk, demo_bomb, demo_bomb_hud, demo_bomb_vis, demo_label, demo_obj, demo_rubble, demo_wreck, direct_hit, dog_portal, dog_portal_armed, dom_capturer, dom_label, dom_point, door, door_back, door_front, door_new, downed_cam, downed_cam_new, downed_hud, downed_hud_new, downed_mannequin, downed_mine_temp, downed_new, downed_spectator, drop_done, drop_int, drop_mag_helper, drop_new, dropped_gun, dying_wish_active, editor_display, element.{barricade, base_coordinates, blue_spawn, boundary, config, destroy, domination, door, editor_exit, editor_save, editor_save_exit, enemy, general_spawn, hardpoint, mission_spawn, mystery_box_pos, out_of_bounds, pap_machine, perk_machine, player_spawn_zb, power_switch, red_spawn, respawn_command, search_and_destroy, special_spawn, start_command, trap, wallbuy, wunderfizz, zb_configure, zb_defaults, zombie_spawn}, exploding, extracting_bullets, ffa_candidate, ffa_top, flash_source, give_class_menu, gm_entity, grenade, grenade_active_effect, grenade_stuck, guardian_golem, hit_dir_marker, hp_label, hp_marker, ik_melee, in_hp_zone, inv_checking, inv_new_drop, inv_restore, inv_slot_owner, inv_swapping, kino, kino.{in_tp, met_active, meteorite_1, meteorite_2, meteorite_3, teleporter_lobby, teleporter_theater}, lure_center, map_editor, map_element, mb_base, mb_bear, mb_can_start, mb_disabled, mb_display, mb_display_new, mb_fs_active, mb_lid, mb_name_reader, mb_new, mb_orig_active, mb_presence, mb_prev_active, mb_shared, mb_temp, mission_enemy, mob_init, mob_lv5, mob_sleeping, model_display, modify_lore, modify_mag_lore, monkey_bomb, mystery_box_active, mystery_box_pos, new, new_element, new_enemy_marker, new_respawn_cmd_marker, new_spawn, new_spawn_marker, new_start_cmd_marker, new_zb_marker, nukable, nuked, oob_point, pap_extracting, pap_extracting_mag, pap_machine, pap_new, pap_owner, pap_weapon_display, perk.quick_revive, perk_machine, pk_new, pk_quick_revive, pool_target, power_switch, power_switch_disp, pu_collecting, pu_item, pu_item_new, pu_text, pump_sound, raycast_target, reading_reserve, refilling_mag, reload_mid_sound, reloading, reloading_weapon, roam_hidden, slow_bullet, snd_alive, snd_bomb, snd_bomb_hud, snd_bomb_vis, snd_carrier, snd_carrier_label, snd_label, snd_loose, snd_loose_at, snd_obj, spawn_candidate, spawn_enemy, spawn_final, spawn_pending, spawn_point, spawn_unlocked, spawn_used, stat_cand, stuck_to_entity, target, temp_dmg_reader, temp_killer, temp_shooter, temp_victim, ticking, to_modify, to_pickup, tombstone, tombstone_new, tp_me, trap_base, trap_center, trap_head, trap_interact, update_lore, username_getter, username_getter_entity, wallbuy, wallbuy_display, wb_new, wb_new_display, wb_reading_mag, wf_active, wf_bear, wf_bear_new, wf_can_start, wf_linked, wf_new, wf_orb_new, wf_prev_active, wunderfizz_machine, wunderfizz_orb, ww_active, xp_earner, xp_winner, zb_dog, zb_dog_new, zb_dying, zb_escort, zb_escort_failed, zb_escort_monkey, zb_escort_new, zb_escort_walk, zb_escorted, zb_frozen_ai, zb_last_roster, zb_near, zb_near_player, zb_near_prev, zb_new, zb_qr_armed, zb_rescued, zb_restart, zb_reviver, zb_rising, zb_sb_cand, zb_scaled, zb_scaling_mag, zb_sprint, zombie_round}; plus the macro families `mgs.{demo_site,dom,dom_label,hp,snd_site}_$(label)`.

## 9. Safety net today

| Net | State |
|---|---|
| Tests | none |
| CI | `.github/workflows/duplicate-code.yml`: jscpd on `src/` (2 clones, 64 lines) |
| `scripts/verify.py` | build + byte snapshot of `build/` in `.refactor/baseline` + byte diff, no normalisation (a comment change is a diff); lint step broken on Linux (`subprocess.run([...], shell=True)` runs a bare `ruff`, exit 2) and reads `../stouputils/pyproject.toml`, absent here; contains `# type: ignore`, U+2192 arrows and U+2026 ellipses |
| Linters configured | ruff, pyright strict, complexipy in `pyproject.toml` (section 7) |
| Command validation | mecha 0.106 ships a 26.3 command tree: parses the 1,617 functions with 0 errors in 97 s and rejects malformed commands (`.refactor/audit/mecha_check.py`) |
| Reference check | `.refactor/audit/dangling.py`: 0 references to missing functions, tags, predicates, loot tables, item modifiers or dialogs |
| Real server | not possible here: `piston-meta.mojang.com` and `launchermeta.mojang.com` (server jar) and the library APIs answer 403 |
| mspt | not measured. On a machine with the game: `/tick query` for mspt, `/debug function mgs:v5.1.0/tick` to list every command one tick executes, `/perf start` / `/perf stop` for a full profile |
