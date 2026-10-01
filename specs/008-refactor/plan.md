# Refactor plan

Numbers come from `audit.md`. "Output" means `build/` as the author's machine produces it. A lot is one commit on `refactor/all`; a lot marked **content** changes what players see or when things happen, and waits for an explicit yes.

## Summary

| Lot | Scope | Current size | Expected gain | Type |
|---:|---|---|---|---|
| 1 | `scripts/verify.py`, `scripts/pyrightconfig.json` | 238 + 6 lines | about +80 source lines; gives normalised diff, mecha check, reference check | safety net |
| 2 | 23 dead functions, 7 dead JSON files, empty `zombies/prep_tick` and its call | 391 output lines, 102 commands | -391 output lines, -103 commands, about -110 Python lines | simplification |
| 3 | 10 objectives never read (5 never written) | 10 `objectives add` + 14 writes | -24 commands, -2 commands per aiming player per tick | simplification |
| 4 | unwired features (D2): lore pipeline, default maps, barricade round reset, `recompute_all` | 352 + about 150 Python lines, 16 functions, 13 load commands | up to -500 Python, -330 output lines | depends on D2 |
| 5 | camo gun models (`database/camo.py`) | 444 files, 2,831,600 lines, 56.5 MB | -2,824,000 output lines, -56.3 MB uncompressed resource pack | simplification |
| 6 | 163 challenge reward functions | 3,586 output lines, 1,793 commands | about -2,400 output lines, -1,620 commands | simplification |
| 7 | 11 unrolled inventory slot scans | about 470 output lines | about -250 output lines, up to -26 commands per call | simplification, medium risk |
| 8 | challenge advancements fired per tick (D4) | 180 tick criteria per player per tick | -180 per player per tick | **content** (timing) |
| 9 | untyped `@e[tag=...]` scans on per-tick paths | 16 in `tick` and `zombies/game_tick`, 18 in editor particles | adds `type=` where one type carries the tag | simplification |
| 10 | tuple tables and boolean flags in the generator | 14 tuple tables, 14 flag parameters | about 0 lines, named fields | simplification |
| 11 | `Any`, `cast`, `pyright: ignore` | 42, 11, 3 | removes those that hide a known type | simplification |
| 12 | docstrings (`stouputils check`) | 2,651 docstring lines, 205 findings | about -300 lines | simplification |
| 13 to 16 | comments, by package: zombies, multiplayer and missions, weapon and shaders, rest | 3,717 comment lines in generator strings, 1,917 Python comments, 448 banned characters | estimated -40 to -60 % of them | simplification |
| 17 | in-game texts (D5) | 25 lang entries, 17 raw em-dashes, 108 box-drawing characters | text recast | **content** |
| 18 | documentation | README 187, `specs/README.md` 34, copilot instructions 10, `upload.py` 58, `weapon_list.txt` 45 | about -100 lines | docs |
| 19 | closure: README, architecture, `CLAUDE.md`, delete `specs/008-refactor/` | | | docs |

Totals if every lot lands as estimated: resource pack about -2.82 M lines (models); mcfunction about -5,000 to -5,800 lines; Python about -3,100 to -4,300 lines; 180 fewer criteria checks per player per tick.

## Decisions to take

| # | Question | Recommendation |
|---|---|---|
| D1 | `build/` is tracked. From this container the build cannot download libraries, so 3 generated files differ, `MCGunsSystem_datapack_with_libs.zip` disappears, and the 312 symlink-mode media files turn into typechanges. What do the lot commits carry? | Each lot commits the source and only the `build/datapack` and `build/resource_pack` files its change touches, computed as (new build) minus (baseline build of the same container); in a library-dependent file such as `en_us.json`, only the lot's own lines are applied on top of the committed version. Zips, `sha1_hashes.json` and `all_items.png` stay untouched; you run one build on your machine before merging and commit it as the last lot. |
| D2 | Unwired features. (a) runtime lore pipeline `utils/update_all_lore` + `lore/*`, never called, sold by the README; (b) Hijacked and Highrise default multiplayer maps behind the uncalled `#mgs:maps/register`, plus `register_map` and 5 empty `hijacked/*` scripts; (c) `zombies/on_round_start`, which would reset the barricade repair cap each round; (d) `progression/recompute_all`, an admin command documented nowhere | (a) delete, with the README line. (b) your call: wiring them adds two maps to existing worlds (content), deleting changes nothing in game. (c) wire it into `#mgs:zombies/on_round_start` as a separate **content** fix, since the comment says per-round. (d) keep, and document it in the README admin commands. |
| D3 | Gameplay bugs found: Double Tap sets `mgs.special.additional_shots` that no shot reads, Juggernaut sets `mgs.special.juggernaut` that nothing reads | Out of this refactor: list them as issues and fix them in their own PR. Lot 3 keeps both objectives. |
| D4 | Lot 8: grant the 180 challenge advancements from the 18 places that change their scores (`minecraft:impossible` criteria plus `advancement grant`), with a catch-up check on join for players whose score already passed a threshold | Yes. Unlocks happen in the same tick, a few commands earlier; only a world updated mid-progress sees the catch-up on next join instead of next tick. |
| D5 | In-game text: recast the 25 lang entries and 17 raw strings with an em-dash; replace the U+2550 and U+2500 `tellraw` banners; keep or drop the U+25C0 and U+25B6 triangles of the Back buttons (`➤` stays, as you said) | Recast with commas or a full stop; banners become a plain coloured line of `=` or are dropped; keep the triangles, they are glyphs like `➤`. |
| D6 | StewBeet-level output this pack does not need: `auto.headers` (11,526 header lines), sniffer source maps shipped in the release zip (1,607 files), `set_items_storage` (7.76 MB written on every load, never read by MGS), `creative_loot_table` | Keep headers (they carry `@within`). Keep source maps out of the release zip and the item storage off for MGS, both as options in StewBeet (a StewBeet PR, outside this one). Keep the creative loot table. |
| D7 | ruff reports 1,877 E501 on mcfunction lines inside generator strings (plus 8 findings of the rules `main` added in `147cee09`: FBT003 3, PERF401 2, RET505 2, SIM300 1, fixed in lots 10 and 11) | Ignore E501 for `src/` in `pyproject.toml`: wrapping commands to 135 columns hurts reading the generated code. Your rules forbid silencing without your say, so this waits for you. |
| D8 | `weapon_list.txt` (a weapon list nothing reads plus a 3-item TODO) and `TODO_26.3_SHADERS.md` (in-game check list, done except Iris) | Delete `weapon_list.txt` after moving the TODO lines to the `specs/README.md` inbox; move the Iris items of `TODO_26.3_SHADERS.md` into `specs/001-shader-migration-263` and delete the root file. |
| D9 | Pull request | Open `refactor/all` as a draft PR after lot 1 so CI (jscpd) runs on every lot; no Claude mention anywhere, commits authored as Stoupy51. |
| D10 | A real-server load test needs `piston-meta.mojang.com`, `piston-data.mojang.com`, `api.modrinth.com`, `cdn.modrinth.com`, `api.smithed.dev` in the environment's allowed hosts | Optional. Without them, lots rely on the normalised diff, mecha and the reference check; you load the pack once on your machine at the end. |

### Answers

| # | Answer |
|---|---|
| D1 | Accepted. |
| D2 | Wire the unwired features, after the author reviews the per-function list. |
| D3 | Juggernaut works (`multiplayer/apply_perks` sets max health to 24; the score is only a flag). Double Tap: no read of `mgs.special.additional_shots` and no damage multiplier found in the build; waiting for the author. |
| D4 | Accepted. |
| D5 | Accepted. The ammo actionbar keeps its special characters. |
| D6 | Only `set_items_storage` goes; headers, source maps and the creative loot table stay. StewBeet has no option for it yet. |
| D7 | Ignore E501. |
| D8 | Accepted. |
| D9 | Accepted: draft PR after lot 1. |
| D10 | The author is looking for the environment setting. |

## Lots

### Lot 1. Safety net

- **Scope**: `scripts/verify.py` (rewrite), `scripts/pyrightconfig.json` (delete if `pyproject.toml` covers it).
- **Change**: `build` runs `stewbeet build`, then deletes the `D:/` folder the livereload plugin creates on Linux (`-s` overrides of `build_copy_destinations` and `require` merge instead of replacing, so they do not prevent it). `baseline` copies `build/datapack` and `build/resource_pack` to `.refactor/baseline/`. `check` builds, then diffs: JSON parsed and compared as data, `.mcfunction` compared command by command (comments and blank lines ignored), `.mcfunction.map` ignored, binaries by hash; it prints added, removed and changed files with the changed commands. `validate` parses every function with mecha's 26.3 tree (in parallel), parses every JSON, and fails on a reference to a missing function, tag, predicate, loot table, item modifier or dialog; it also prints the unreachable functions. `lint` runs ruff, pyright strict with the venv interpreter, complexipy. No `shell=True`, no sibling-folder config.
- **Gain**: none on the pack. Source about +80 lines net.
- **Type**: safety net.
- **Risk**: low. **Verification**: `check` on an unchanged tree prints an empty diff; `validate` on a copy with a deleted function and predicate reports them (done once in the audit, 19 hits); a comment-only edit gives an empty `check`.
- Tests: the generator's only behaviour is its output, so the snapshot diff plus mecha plus the reference check are its regression tests. Doctests come with the lots that touch a pure helper.

### Lot 2. Dead functions and data

- **Scope** (under `src/functional/` unless noted): `helpers/dialogs.py` (wrapper only where called: `dialogs/config`, `dialogs/{missions,multiplayer,zombies}/setup`), `multiplayer/maps.py` (`store_loaded_idx`), `zombies/player/inventory/hooks.py` (`recreate_critical_items`), `zombies/machines/pap/magazines.py` (`refill_matching_magazines`), `zombies/machines/pap/lore.py` (`set_item_name`), `zombies/objects/wallbuys/give.py` (`count_guns`, `lookup_magazine_id`), `zombies/objects/wallbuys/hover.py` (`render_hover_title`), `zombies/player/revive/setup.py` (predicate `input/any`), `src/config/blocks/materials.py` (`air`), `world.py` (`jump`, `fence_gate`), `surfaces.py` (`activate`), `sounds.py` (`sounds/special_sound`), `zombies/rewards/powerups/drops.py` (loot table `zombies/powerup_drop`), `zombies/game/lifecycle/start.py:151` (empty `zombies/prep_tick`) and its call in `zombies/game/lifecycle/tick.py:22`.
- **Change**: delete them and anything only they used.
- **Gain**: output -24 functions, -7 JSON files, about -391 lines, -103 commands, one storage test less per tick while a zombies game prepares; Python about -110 lines.
- **Type**: simplification. **Risk**: low (versioned internal paths, no caller, no data reference). **Verification**: `check` shows only the listed files removed and the one `tick` line; `validate` reports 0 missing references and 14 unreachable functions left (lot 4's).

### Lot 3. Objectives never read

- **Scope** (under `src/functional/`): `main/objectives.py` (`mgs.player`, `mgs.zoom_timer`, `mgs.switch_cooldown` creation), `weapon/hud/zoom.py` (4 `zoom_timer` writes), `weapon/ammo/switch.py` (`switch_cooldown` write), `missions/game/setup.py` (`mgs.mi.timer`, `mgs.mi.total_enemies`), `multiplayer/game/setup.py` (`mgs.mp.timer`), `multiplayer/gamemodes/__init__.py` (`mgs.mp.gm_timer`), `multiplayer/loadouts/storage.py`, `loadouts/editor/{save,hub}.py`, `loadouts/actions/manage.py` (`mgs.mp.edit_step`), `zombies/machines/perks/tombstone.py` and `zombies/player/whos_who.py` (the save loops skip their own perk, so `mgs.zb.tsp.tombstone` and `mgs.zb.wwp.whos_who` are no longer written).
- **Change**: stop creating and writing them. No rename: existing worlds keep the objectives, unused.
- **Gain**: -10 `objectives add`, -14 writes, -2 commands per player holding a gun per tick (`zoom/main`).
- **Type**: simplification (frozen ids are only dropped, never renamed). **Risk**: low; an external pack reading one of them would break, none is documented. **Verification**: `check` shows only those lines gone; grep of the output for the 10 names is empty.

### Lot 4. Unwired features (after D2)

- **Scope**: `src/functional/weapon/ammo/lore/` (352 lines), `multiplayer/maps.py` (`default_maps`, `register_map`, hijacked scripts and calls), `progression/__init__.py` (`recompute_all`), README lines.
- **Change**: per D2. Wiring `zombies/on_round_start` goes in its own **content** commit, not here.
- **Gain** (all deletions): Python about -500 lines; output -16 functions, about -330 lines and 13 load commands, storage `mgs:lore_templates` no longer written.
- **Type**: simplification for deletions. **Risk**: low. **Verification**: `check` lists only the removed files, the 13 load lines and the tag `#mgs:maps/register`.

### Lot 5. Camo models as child models

- **Scope**: `src/database/camo.py` (`retexture`, `add_camo_variant`).
- **Change**: a camo variant model becomes `{"parent": "mgs:item/<gun>", "textures": {...}}` instead of a full copy of the base model. Zoom variants already work this way.
- **Gain**: resource pack -444 x 6,377 lines on average: 2,831,600 to 7,344 lines, 56.5 MB to 0.21 MB uncompressed. Download size of the resource pack zip measured after the build.
- **Type**: simplification (Minecraft resolves `elements`, `display` and `gui_light` through `parent`). **Risk**: medium: StewBeet's isometric renderer and `all_items.png` read models and may not follow `parent`. **Verification**: a one-off check in `.refactor/` resolves every child against its parent and compares it to the baseline model (must be equal); `check` lists only the 444 model files; `all_items.png` and `iso_renders/` unchanged; you look at three camo guns in game.

### Lot 6. Challenge reward macro

- **Scope**: `src/functional/progression/advancements/` (reward writer), output `progression/adv/**/reward_*`.
- **Change**: one macro function `progression/adv/reward` with the 11 commands; each `reward_N` becomes one line passing title key, description key, XP, branch, chain, tier and side. Runs only on unlock, so the macro cost does not matter.
- **Gain**: 163 functions from 11 commands to 1: -1,620 commands, about -2,400 output lines; Python about -10 lines.
- **Type**: simplification. **Risk**: low. **Verification**: a one-off script expands the macro with each call's arguments and compares the result with the baseline body (must be equal for all 163); `check` lists only those files plus the new macro.

### Lot 7. Inventory slot scans as range checks

- **Scope**: generators of `ammo/inventory/{find,has_ammo}`, `ammo/reserve/scan`, `zombies/pap/pap_upgrade_magazines`, `zombies/bonus/max_ammo(_reload_weapons)`, `shared/drops/give_mag`, `multiplayer/perks/scavenger_refill`, `ammo/update_old_weapon`, `zombies/inventory/enforce_slot`.
- **Change**: where a function only needs "does any slot hold X", one `execute if items entity @s container.* *[...]` replaces 27 per-slot lines; functions that act per slot or rely on slot order stay unrolled. Decided per function after reading it.
- **Gain**: up to -26 commands per call and about -250 output lines.
- **Type**: simplification. **Risk**: medium (slot coverage and order). **Verification**: per function, the slot list covered before and after is printed and compared; `check` lists only these functions.

### Lot 8. Challenge advancements without per-tick criteria (after D4)

- **Scope**: `src/functional/progression/advancements/` (criteria), the 18 writers of the 14 `mgs.adv.*` scores, the level-up functions for level challenges, the join path.
- **Change**: criteria become `minecraft:impossible`; each score change calls the check function of its chain, which grants every tier whose threshold is reached; join runs all chain checks once.
- **Budget**: before, up to 180 criteria checks per player per tick; after, 0 per tick, plus one check function per score change.
- **Type**: **content** (unlock moment moves inside the same tick; catch-up on join). **Risk**: medium. **Verification**: `check` shows criteria and the added calls only; a one-off script lists, for every advancement, its threshold before and after (must be equal).

### Lot 9. Typed selectors on per-tick paths

- **Scope**: `tick` (`mgs.grenade` and `mgs.slow_bullet` live on `item_display` only), `zombies/game_tick` (12), `maps/editor/particles` (18, markers), after checking every summon site of each tag.
- **Change**: add `type=` where a single entity type ever carries the tag; leave mixed-type tags alone.
- **Budget**: static count of untyped tag scans on these paths, 34 before, target 0 to 10 after; real mspt only measurable on your machine (`/tick query`, `/debug function mgs:v5.1.0/tick`).
- **Type**: simplification. **Risk**: low once each tag's summon sites are listed. **Verification**: per tag, the list of entity types summoned with it; `check` lists only selector changes.

### Lot 10. Generator data as dataclasses

- **Scope**: the 14 tuple tables (`zombies/common.py`, `helpers/dialogs.py`, `multiplayer/game/sidebar.py`, `database/camo.py`, `database/items.py`, `weapon/firing/sound.py`, `zombies/menus.py`, `zombies/machines/mystery_box/setup.py`) and the 14 boolean flag parameters.
- **Change**: frozen dataclasses built with one keyword constructor call per row; flags become named values or disappear when only one caller passes them.
- **Gain**: about 0 lines. **Type**: simplification. **Risk**: low. **Verification**: `check` empty, pyright strict 0.

### Lot 11. Typing

- **Scope**: the 42 `Any`, 11 `cast`, 3 `pyright: ignore` in `src/`.
- **Change**: use `JsonDict` and friends from `stouputils.typing`, real types where StewBeet exposes them; keep a `cast` only when it states a true invariant.
- **Type**: simplification. **Verification**: `check` empty, pyright strict 0.

### Lot 12. Docstrings

- **Scope**: every `src/` file flagged by `stouputils check` for typed-argument (165), examples-header (29), long-docstring (11), module-docstring-position (1), constant-comment (6), and docstrings that narrate the past.
- **Change**: entries that rephrase a name or repeat a type go; docstrings say what the caller needs.
- **Gain**: about -300 lines. **Type**: simplification. **Verification**: `check` empty, `stouputils check` clean on touched files.

### Lots 13 to 16. Comments (generator and generated)

- **Scope**: 13 `src/functional/zombies` (2,723 comment lines), 14 `multiplayer` and `missions` (1,402), 15 `weapon`, `shaders`, `stamina.py`, `player_config.py`, `mob_ai.py` (about 1,250), 16 everything else (about 900).
- **Change**: keep a comment only when a reader would get something wrong without it (an order that matters, an engine limit). Delete paraphrases, banners, section labels inside functions, past narration; fix banned characters in what stays.
- **Gain**: estimated -40 to -60 % of the scope's comment lines, the same in the generated `.mcfunction`; the heuristic's lower bound is 529 lines.
- **Type**: simplification. **Verification**: `check` empty (comments are ignored by the normalised diff), raw diff shows comment lines only, `stouputils check` clean on touched files.

### Lot 17. In-game texts (after D5)

- **Scope**: strings in `src/` behind the 25 lang entries, the 17 raw em-dashes (`refresh_sidebar_demo` and others), the box-drawing banners in `missions/victory`, `zombies/game_over`, `snd/start_round`, `demo/start_round`.
- **Change**: recast per D5. StewBeet derives lang keys from the text, so changed lines get new keys in `en_us.json`.
- **Type**: **content**. **Verification**: `check` lists only the text lines and the lang file; the baseline is updated after your approval.

### Lot 18. Documentation

- **Scope**: `README.md`, `specs/README.md`, `.github/copilot-instructions.md`, `upload.py`, and per D8 `weapon_list.txt`, `TODO_26.3_SHADERS.md`.
- **Change**: remove claims the code does not back (runtime lore if lot 4 deletes it), the French summary, the kill cam design note (already in `specs/004`), the dead link and stale states of `specs/README.md`, the 26.1 mention, the foreign summary and commented-out code of `upload.py`.
- **Type**: docs. **Verification**: every remaining claim checked against the code; `stouputils check` clean.

### Lot 19. Closure (phase 4)

- README: install, build, run, use, then a short architecture section. `CLAUDE.md`: build, verify and load commands, conventions, frozen ids. Before and after table in the final report. `specs/008-refactor/` deleted in the last commit.
