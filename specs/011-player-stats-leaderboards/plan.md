# Implementation Plan: Player Stats, Leaderboards, Zombies Knife Camos and Mystery Box Pools

**Branch**: `011-player-stats-leaderboards` | **Date**: 2026-10-31 | **Spec**: [spec.md](spec.md)

Four phases, in this order. Leaderboards come last on purpose: they read everything the earlier phases record.

| Phase | Content | Depends on | Status |
|---|---|---|---|
| P1 | Identity, stats recording, snapshot, Quick Actions, stats dialogs | Nothing | Built; tested over RCON, client checks open |
| P2 | Zombies knife camos by level | P1 (Player Settings button) | Built; pick and lock tested over RCON |
| P3 | Configurable mystery box pool | Nothing: independent, can be done at any time | Built; tested over RCON |
| P4 | Leaderboards, dialogs, holograms, records, admin resets | P1 | Built; tested over RCON |

Every phase ends with `uv run python scripts/verify.py validate`, `lint`, `server --java <java 25>` and the in-game tests listed, on a local server driven over RCON. Its decisions are added to `spec.md` as they settle, and its line in `specs/README.md` is updated.

## P1: Identity, stats and Quick Actions

**Depends on**: nothing. **Status**: built (`src/functional/stats/`).
Tested on a local server over RCON: the UUID key, first login and backfill, a simulated rename (scores, `bs.id` and `mgs.mp.pid` follow, an unset score never overwrites), a case-only rename, an offline roster player snapshotted at a game end, the award-fed counters, the three stats pages (values, K/D, win rate, time) and the admin reset.
Open: the dialogs seen in a client, and a full game with a real player. Both test clients crashed on joining (NTSTATUS 0xC0000005) during this session.

1. Check in game that a macro writes and reads `mgs:stats players."[I;a,b,c,d]".name` with a real UUID (negative ints included). If it fails, pick another key form before writing anything else and record it in the spec.
2. One Python constant listing every persistent per-player objective (`mgs.mp.xp_*`, `mgs.zb.xp_*`, `mgs.adv.*`, `mgs.st.*`, `mgs.player.*` toggles, `mgs.mp.class`, `mgs.zb.knife_camo` once P2 adds it, `bs.id`).
3. Login hook on a new `mgs.st.login` (`custom:leave_game`) objective, plus the first join: read UUID and name, append to `known` and backfill `players."<uuid>"` from the existing scores the first time, migrate scores on a rename (spec: Identity), update `name`.
4. Declare the new `mgs.st.*` objectives and feed them at the existing award sites (`zombies/xp.py`, `multiplayer/xp.py`, `missions/xp.py`, and the sites with no award: downs, bleed-outs, boxes opened, deaths, losses, games, per gamemode games and wins).
5. Count `time` per mode in `progression/tick_player`.
6. Snapshot write: one function per mode copying the roster's scores into `players."<uuid>"`, called at `zombies/game_over`, `#mgs:multiplayer/on_game_end` and the Missions end (victory and stop), offline roster players included (by name).
7. Quick Actions: `mgs:open_menu` runs `/trigger mgs.player.config set 1`.
8. Player Settings gains My Stats and Players; dialogs: stats of a player per mode (K/D, win rate and points computed at display), known players paged by 10.
9. Admin dialog: reset one player's stats (scores and snapshot, levels untouched).
10. In-game tests: fresh player, player with old scores (backfill), rename and case-only rename (levels, challenges and custom loadouts kept), player leaving mid-game then the game ending, stats of an offline player, Quick Actions key.

## P2: Zombies knife camos

**Depends on**: P1 (the Knife Camo button lives in Player Settings, and `mgs.zb.knife_camo` joins the rename list). **Status**: built (`zombies/player/knife_camo.py`, levels in `CamoVariant.zb_knife_level`).
Tested over RCON: picking an unlocked camo, refusing a locked one, the picker rows. Open: the knife model in a client, the unlock message.

1. Thresholds table (Default 1, Autumn 25, Galaxy 50, Red Polymer 75, Gold 100) as one constant next to `CAMO_VARIANTS`.
2. `mgs.zb.knife_camo` score; Knife Camo dialog with locked entries showing their level; picking a locked one is refused.
3. Zombies starting knife and bleed-out respawn knife use the picked camo's model, keeping vanilla reach.
4. Unlock message on `#mgs:progression/on_level_up` for the Zombies side.
5. Update the `progression/__init__.py` docstring ("nothing is gated behind a level").
6. In-game tests: each threshold with `scoreboard players set` on the level then `progression/zb/recompute` or the level-up path, start a game, bleed out and respawn, a locked pick.

## P3: Configurable mystery box pool

**Depends on**: nothing, independent of P1, P2 and P4. **Status**: built (`mystery_box/setup.py`, `pool_menu.py`; editors in the Zombies setup menu).
Tested over RCON: default pool from the catalog weights, a map override (weight 0 and an unknown id left out), the Ray Gun boost found by id, saving the global and the map pool from dialog-shaped values, clearing the override, the editor's inputs. The pool is built in `zombies/start` before `#mgs:zombies/register_mystery_box_item`, so registered items now stay. The map editor needs no change: it saves the map compound it loaded, extra fields included.
Open: a pull and a collect with a real player.

1. Pool entry becomes `{weapon_id, weight}`; drop `give_function` and `collect.py`'s macro call, give by `weapon_id` (monkey bomb to the tactical slot, everything else through the weapon give, with magazine data from a build-time table).
2. Global default `mgs:config zombies.mystery_box_pool`, created when absent with every weapon at its catalog weight.
3. Per map override `mystery_box_pool` in the Zombies map data, kept by the map editor's save and load.
4. Build the active pool once at game start; delete `ensure_default_pool` and its call in `try_use`.
5. `weigh_ray_gun` finds the Ray Gun by `weapon_id` at pool build; no Ray Gun in the pool means no boost.
6. Admin dialog: every catalog weapon with on/off and weight, for the global pool or the current map's override.
7. In-game tests: default pool unchanged in behaviour, a map override with three weapons, every weapon excluded (`deny_pool_empty`), Ray Gun excluded, Ray Gun dry-pull boost still working, fire sale.

## P4: Leaderboards

**Depends on**: P1 (snapshot, identity, end-of-game hooks). **Status**: built (`src/functional/stats/boards.py`, element `leaderboard` in `map_editor_defs.py`).
Tested over RCON: level boards, a Zombies map board with its player-count buckets (a worse round keeps the old entry, a better one moves it up), Missions times (lower first, only after a victory), every dialog page with the filters and the viewer's rank, a hologram placed from map data, shown, titled and hidden with no player near, the admin reset.
Holograms exist on Zombies maps only, the editor element being a Zombies one. The filter buttons offer All and 1 to 4 players.
Open: the "New record!" line and the dialogs seen in a client, a hologram placed in the editor.

1. Insertion helper: remove the entry by UUID, walk once to the insertion point, insert, return the rank. Descending for rounds and levels (tie on XP), ascending for Missions times.
2. Updates at the game ends written in P1: `zb_map` (`all` and the player count bucket), `mi_map` (victory only, `#mi_timer`), `level_mp` and `level_zb`; levels also at login.
3. "New record!" line with the rank at Zombies game over.
4. Leaderboards dialog: board, then map and player count filter, top 10 and the viewer's rank; button in Player Settings.
5. Map editor element `leaderboard` (board, map id, player filter), its display marker and names like the other elements (spec 010).
6. Hologram tick once a second: summon the `text_display` when a player is within 24 blocks, kill it otherwise; an update kills the displays so they rebuild.
7. Admin dialog: reset one map's Zombies or Missions leaderboard.
8. In-game tests: solo then duo games on the same map (buckets and `all`), equal rounds, a renamed player showing under the new name, an offline player's entry, a mission time, holograms appearing, refreshing after a game and disappearing, F3+L with several holograms placed.
