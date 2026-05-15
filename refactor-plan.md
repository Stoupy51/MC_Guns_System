# Refactor Plan - Duplicate Logic Audit

Scope audited: `src/**/*.py` (source only, excluding generated `build/`).

## Inventory

### 1) Cross-mode game start guard pattern
- Locations:
  - `src/functional/multiplayer/game.py:58`
  - `src/functional/missions/game.py:52`
  - `src/functional/zombies/game.py:71`
- What it does: prevents starting a mode when the mode is already `active` or `preparing`, and emits mode-specific error text.
- Diff-style differences:
  - Common: `game_start_guards(ns, <storage>, <mode_name>)`
  - Diff: storage key/value only (`multiplayer`/`missions`/`zombies` and display label text).
- Similarity: 98%
- Classification: [PARAM]
- Recommendation: 1. Refactor

### 2) `load_map_from_storage` wrappers are nearly identical
- Locations:
  - `src/functional/multiplayer/game.py:196`
  - `src/functional/missions/game.py:178`
  - `src/functional/zombies/game.py:151`
- What it does: delegates to shared map loader macro with mode/id.
- Diff-style differences:
  - Common: `$function {ns}:v{version}/shared/maps/load {id:"$(map_id)",mode:"...",override:{}}`
  - Diff: only `mode` string value differs.
- Similarity: 99%
- Classification: [PARAM]
- Recommendation: 2. Wrap (single helper generator for mode wrappers)

### 3) Startup pipeline duplicated across modes (`start`)
- Locations:
  - `src/functional/multiplayer/game.py:60`
  - `src/functional/missions/game.py:54`
  - `src/functional/zombies/game.py:73`
- What it does: map existence checks, load selected map, copy map into mode storage, set state `preparing`, reset mode/player scores, set gamerules, load base coords/bounds, preload schedule + announcement.
- Diff-style differences:
  - Common: load map -> set preparing -> reset per-mode scores -> setup base/bounds -> schedule preload.
  - Diff: zombies has points/perk systems and night settings; missions has coop/team coercion + forceload; multiplayer has gamemode setup and sidebar prep.
- Similarity: 78%
- Classification: [WRAPPER]
- Recommendation: 2. Wrap (extract shared `mode_start_common(mode_config)` core; keep mode-specific hooks)

### 4) Legacy respawn/start command normalization duplicated in two modes
- Locations:
  - `src/functional/multiplayer/game.py:67`
  - `src/functional/missions/game.py:64`
- What it does: backward-compat normalization for `respawn_command`/`respawn_commands` and `start_commands` formats.
- Diff-style differences:
  - Common: same 5-line compatibility block.
  - Diff: storage prefix only (`multiplayer` vs `missions`).
- Similarity: 97%
- Classification: [PARAM]
- Recommendation: 1. Refactor

### 5) Preload completion scheduling duplicated
- Locations:
  - `src/functional/missions/game.py:122`
  - `src/functional/zombies/game.py:144`
- What it does: schedules `preload_complete` after 20 ticks post warmup teleport.
- Diff-style differences:
  - Common: `schedule function .../preload_complete 20t`
  - Diff: mode path only.
- Similarity: 99%
- Classification: [PARAM]
- Recommendation: 1. Refactor

### 6) Prep freeze/effects block duplicated across all 3 modes
- Locations:
  - `src/functional/multiplayer/game.py:168`
  - `src/functional/missions/game.py:149`
  - `src/functional/zombies/game.py:179`
- What it does: applies darkness/blindness/night_vision/saturation and movement/jump lock during preparation.
- Diff-style differences:
  - Common: same freeze/effect skeleton.
  - Diff: zombies adds knockback/max_health adjustments; missions resets waypoint range; multiplayer omits those extras.
- Similarity: 84%
- Classification: [FLAG]
- Recommendation: 1. Refactor

### 7) End-prep unfreeze transitions duplicated (missions/zombies)
- Locations:
  - `src/functional/missions/game.py:189`
  - `src/functional/zombies/game.py:203`
- What it does: guard state, set active, restore movement, clear prep effects, keep saturation, then branch into mode-specific start action.
- Diff-style differences:
  - Common: active transition + movement/effect restoration.
  - Diff: missions spawns all enemies + compass; zombies starts round logic.
- Similarity: 82%
- Classification: [HOOK]
- Recommendation: 1. Refactor

### 8) Respawn countdown hook reused with mode-specific target
- Locations:
  - `src/functional/multiplayer/game.py:421`
  - `src/functional/missions/game.py:340`
- What it does: injects same countdown tick logic and calls mode-specific actual respawn function.
- Diff-style differences:
  - Common: `respawn_countdown_tick_lines(ns, <prefix>, <respawn_fn>)`
  - Diff: prefix (`mp` vs `mi`) and callback function path.
- Similarity: 96%
- Classification: [PARAM]
- Recommendation: 2. Wrap

### 9) Stop/cleanup pipeline duplicated across all modes
- Locations:
  - `src/functional/multiplayer/game.py:201`
  - `src/functional/missions/game.py:420`
  - `src/functional/zombies/game.py:351`
- What it does: return state to lobby, clear schedules, restore player attributes/effects, kill mode entities, disable mode tags/flags, remove class menu tag, announce end.
- Diff-style differences:
  - Common: same cleanup skeleton.
  - Diff: mode-specific entities/scoreboards/sidebar and additional cleanup (forceload, time rule, team cleanup).
- Similarity: 76%
- Classification: [WRAPPER]
- Recommendation: 2. Wrap

### 10) Late-join flow duplicated across modes
- Locations:
  - `src/functional/multiplayer/game.py:259`
  - `src/functional/missions/game.py:469`
  - `src/functional/zombies/game.py:405`
- What it does: active-game guard, anti double-join, initialize player state, apply class, teleport, call map join script, announce join.
- Diff-style differences:
  - Common: same sequence and checks.
  - Diff: per-mode score setup and equipment (compass/points/perks/team assignments).
- Similarity: 80%
- Classification: [WRAPPER]
- Recommendation: 1. Refactor

### 11) Spawn marker generation stack duplicated (`summon_spawns`/`summon_spawn_iter`/`summon_spawn_at`)
- Locations:
  - `src/functional/multiplayer/game.py:541`, `:558`, `:585`
  - `src/functional/missions/game.py:509`, `:516`, `:538`
  - `src/functional/zombies/game.py:544`, `:560`, `:588`
- What it does: iterate relative spawns, convert to absolute using base coords, store macro args, summon marker.
- Diff-style differences:
  - Common: identical iterator + coordinate transformation pattern.
  - Diff: source data schema differs (`[x,y,z,yaw]` vs object with `pos/rotation`), zombies adds `group_id` scoring.
- Similarity: 74%
- Classification: [SUBCLASS]
- Recommendation: 1. Refactor

### 12) Spawn selection/teleport stack duplicated (`tp_all_to_spawns`/`pick_spawn`/`tp_to_spawn`/`respawn_tp`)
- Locations:
  - `src/functional/multiplayer/game.py:592`, `:608`, `:694`, `:712`
  - `src/functional/missions/game.py:543`, `:549`, `:566`, `:580`
  - `src/functional/zombies/game.py:594`, `:599`, `:616`, `:630`
- What it does: choose candidate spawns, select one (random or weighted), teleport pending player, fallback on respawn.
- Diff-style differences:
  - Common: same pending/candidate tagging + teleport macro sequence.
  - Diff: multiplayer adds enemy-distance optimization and team-aware type routing; missions/zombies use simpler random selection.
- Similarity: 72%
- Classification: [WRAPPER]
- Recommendation: 2. Wrap (shared random strategy + optional advanced strategy flag)

### 13) Boundary checking duplicated between mode-specific and shared implementations
- Locations:
  - `src/functional/multiplayer/game.py:482`
  - `src/functional/core/bounds.py:92`
- What it does: read player position, compare against min/max bounds, enforce OOB kill.
- Diff-style differences:
  - Common: same position extraction + axis comparisons.
  - Diff: multiplayer routes to `simulate_death` path (`bounds_kill`/`oob_kill`) for kill tracking; shared version directly applies `damage ... out_of_world`.
- Similarity: 86%
- Classification: [HOOK]
- Recommendation: 1. Refactor

### 14) Setup menus duplicated across multiplayer/missions/zombies
- Locations:
  - `src/functional/multiplayer/menus.py:59`
  - `src/functional/missions/menus.py:29`
  - `src/functional/zombies/menus.py:28`
- What it does: render mode setup UI with map selection and action buttons.
- Diff-style differences:
  - Common: same menu frame and button layout pattern.
  - Diff: multiplayer has extra gamemode/score/time/team controls.
- Similarity: 71%
- Classification: [SUBCLASS]
- Recommendation: 1. Refactor

### 15) Map select menu boilerplate duplicated across multiplayer/missions/zombies
- Locations:
  - `src/functional/multiplayer/menus.py:74`
  - `src/functional/missions/menus.py:40`
  - `src/functional/zombies/menus.py:39`
  - Shared target used by all: `src/functional/core/map_menus.py:10`
- What it does: setup `_map_iter`, `_map_select_mode`, run shared iterator, print no-map message.
- Diff-style differences:
  - Common: almost identical preamble/iterator/footer.
  - Diff: storage namespace and empty-list message text/color.
- Similarity: 92%
- Classification: [PARAM]
- Recommendation: 1. Refactor

### 16) Map script call-wrapper generation duplicated
- Locations:
  - `src/functional/multiplayer/maps.py:57`, `:61`
  - `src/functional/zombies/maps.py:20`, `:24`
- What it does: build `guard` and emit `calls/{script}` wrappers for start/tick/join/leave/respawn (plus power in zombies).
- Diff-style differences:
  - Common: same guard-then-delegate wrapper loop.
  - Diff: map id/mode/storage names; zombies adds `power` call.
- Similarity: 93%
- Classification: [PARAM]
- Recommendation: 1. Refactor

### 17) Team-scoring kill hooks duplicated across TDM/DOM/HP
- Locations:
  - `src/functional/multiplayer/gamemodes/team_deathmatch.py:24`
  - `src/functional/multiplayer/gamemodes/domination.py:197`
  - `src/functional/multiplayer/gamemodes/hardpoint.py:145`
- What it does: increment personal kill, increment team score by team id, refresh sidebar.
- Diff-style differences:
  - Common: same 3 scoring lines + refresh.
  - Diff: DOM refreshes DOM-specific sidebar; TDM/HP differ only by trailing win check behavior.
- Similarity: 90%
- Classification: [WRAPPER]
- Recommendation: 2. Wrap

### 18) Relative->absolute coordinate conversion repeated in multiple systems
- Locations:
  - `src/functional/core/spawning.py:18`
  - `src/functional/multiplayer/gamemodes/domination.py:46`
  - `src/functional/multiplayer/gamemodes/hardpoint.py:42`
  - `src/functional/multiplayer/gamemodes/search_and_destroy.py:42`
  - `src/functional/missions/game.py:235`
- What it does: read relative coords, add base offsets, store into storage macro payload.
- Diff-style differences:
  - Common: same scoreboard math + temp storage write pattern.
  - Diff: source path and destination temp object names differ.
- Similarity: 83%
- Classification: [SUBCLASS]
- Recommendation: 1. Refactor

### 19) Zombies deny-not-enough-points handlers mostly unified, one outlier remains
- Locations:
  - Unified helper: `src/functional/zombies/common.py:13`
  - Consumers: `src/functional/zombies/doors.py:132`, `src/functional/zombies/perks.py:206`, `src/functional/zombies/traps.py:149`, `src/functional/zombies/wallbuys.py:159`, `src/functional/zombies/pap.py:548`
  - Outlier duplicate: `src/functional/zombies/mystery_box.py:278`
- What it does: prints not-enough-points message + deny sound.
- Diff-style differences:
  - Common: identical message shape and follow-up sound.
  - Diff: mystery box hardcodes score source (`#zb_mystery_box_price` in config objective) and bypasses helper.
- Similarity: 88%
- Classification: [PARAM]
- Recommendation: 1. Refactor

### 20) Intra-file slot-specific purchase/refill blocks duplicated in wallbuys
- Locations:
  - Core block root: `src/functional/zombies/wallbuys.py:245`
  - Slot variants at: `:248`, `:253`, `:258` and similarly `:355`, `:361`, `:367`
- What it does: repeats same purchase/refill flow for slots 1/2/3 with only slot indexes changing.
- Diff-style differences:
  - Common: identical check->same-weapon->reload/replace sequence.
  - Diff: slot literals (`1`,`2`,`3`) and corresponding `hotbar`/`inventory` numbers.
- Similarity: 95%
- Classification: [PARAM]
- Recommendation: 1. Refactor

### 21) Module orchestrator functions are repeated boilerplate
- Locations:
  - `src/link.py:18`
  - `src/functional/multiplayer/__init__.py:12`
  - `src/functional/missions/__init__.py:8`
  - `src/functional/zombies/__init__.py:25`
  - `src/functional/core/__init__.py:11`
  - `src/functional/weapon/__init__.py:19`
- What it does: sequentially calls module generator functions.
- Diff-style differences:
  - Common: plain ordered call lists.
  - Diff: function lists and order only.
- Similarity: 68%
- Classification: [INLINE]
- Recommendation: 4. Leave
- Justification for Leave: a generic registry would hide generation order dependencies and increase indirection for little gain.
  - Minimal sketch showing added complexity:
    - `for fn in REGISTRY['zombies']: fn()` plus maintenance of ordered registries per mode.

## Notes on deferred/leave decisions
- Only item 21 is marked Leave with explicit complexity justification.
- No Defer items were assigned because no concrete blocker (like missing tests) is required to begin extraction on these duplicates.
