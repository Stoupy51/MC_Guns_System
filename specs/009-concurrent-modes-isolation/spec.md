# Feature Specification: Isolation of Concurrent Multiplayer, Missions and Zombies Games

**Feature Branch**: `009-concurrent-modes-isolation`

**Created**: 2026-10-16

**Status**: B1 to B10, L1, L3, L5, L6, FR-012 and FR-015 built. Played with two clients: a match stopped beside a zombies run in another dimension left the run whole, and no message crossed. L4 and the tab list (`setdisplay list`, server-wide) are open.

**Input**: Can one Multiplayer match, one Missions run and one Zombies run play at the same time on one
server without interfering: messages, kills, scores, and everything else? Progression and achievements
may be shared. Two games of the same mode at once are not supported and stay out of scope.

## Audit

Read from the sources on 2026-10-16. Each finding names where it lives and what goes wrong when two
modes run together. "Breaks" means a game is corrupted or ended; "leaks" means players see or hear
something from another game.

### Breaks

| # | Finding | Where | Effect |
|---|---|---|---|
| B1 | Every stop kills `@e[tag=mgs.gm_entity]`, a tag all three modes put on their entities. | `multiplayer/game/stop.py`, `missions/game/stop.py`, `zombies/game/lifecycle/over.py` | Ending a mission deletes the zombies map: doors, boxes, perk machines, the zombies themselves. Ending a match deletes the mission enemies. |
| B2 | Map bounds `#bound_x1..#bound_z2` and map base `#gm_base_x/y/z` are single global scores, loaded at each mode's start. | `core/bounds.py`, `core/commands.py`, `zombies/game/lifecycle/stuck.py` | Starting a match overwrites the zombies bounds, and zombies players outside the match's box get `full_death` for out of bounds. Map scripts (`call_script_at_base`) run at the last loaded base. |
| B3 | Zombies start sets `mgs.mp.in_game` and `mgs.mi.in_game` to 0 for `@a`. | `zombies/game/lifecycle/start.py` | Starting zombies removes every player from a running match and mission. |
| B4 | The multiplayer kill signal only checks that a match is active, not that the killer is in it. | `multiplayer/game/death.py` (`on_kill_signal`) | A zombies or missions kill adds `mp.kills`, and in FFA can make that player win the match. In TDM it can add team points. |
| B5 | `#any_game_active` is one flag set by every start and cleared by every stop. | `helpers/lifecycle.py` | Stopping one mode turns off custom regen, hurt effects and stamina for the modes still running. |
| B6 | Each stop runs `player/fx_reset` and stamina and hunger resets on `@a`. | `helpers/lifecycle.py` (`regen_disable_lines`) | Ending a mode strips scopes, crosshairs and flashes from players of the other modes. |
| B7 | Gamerules are global: `natural_health_regeneration`, `keep_inventory`, `immediate_respawn`, `advance_time`, `max_entity_cramming`, `spawn_mobs`; zombies also runs `time set 18000`. | `helpers/lifecycle.py`, every `start.py` and `stop.py`, `zombies/enemies/escort/hooks.py` | Ending one mode turns natural regen back on for the others. Zombies freezes the time of day for everyone. |
| B8 | `mgs.mp.death_count` and `mgs.mp.spectate_timer` are shared, and each start resets them on `@a`. | every `start.py`, `zombies/player/revive/down.py` | A start in one mode can cancel a respawn or spectate timer in progress in another. |
| B9 | Missions players join the `mgs.blue` team with `mp.team=1`, and the match stop and the FFA setup run `team leave @a[team=mgs.blue]` and reset `mp.team` on `@a`. | `core/player_menus.py`, `missions/game/stop.py`, `multiplayer/game/stop.py`, `multiplayer/gamemodes/free_for_all.py` | Starting an FFA or ending a match takes mission players out of their team. |
| B10 | Map scripts are entries of one function tag per script (`#mgs:maps/tick_script`), each guarded only by its own mode's state and map. | `core/commands.py`, `zombies/maps.py`, `multiplayer/maps.py` | The zombies tick runs the match map's tick script too, at the zombies base, and the reverse. |

### Leaks

| # | Finding | Where | Effect |
|---|---|---|---|
| L1 | About 100 `tellraw @a`, `title @a` and `playsound ... @a` without a mode filter. | Mostly `multiplayer/` (bomb modes, rounds, wins), zombies round banners and admin messages, missions start and end | Everyone on the server reads the other games' rounds, wins, bomb plants and join messages. |
| L2 | Join announcements use `tellraw @a`. | `helpers/lifecycle.py` (`late_join_flow_lines`) | Everyone sees who joined which game. Wanted: they stay server-wide. |
| L3 | `scoreboard objectives setdisplay sidebar` and `list` are server-wide, and both multiplayer (`mgs.sidebar`) and zombies (`mgs.zb_sidebar`) set them. | `multiplayer/game/sidebar.py`, `multiplayer/game/start.py`, `zombies/game/lifecycle/sidebar.py` | The last mode to refresh its sidebar wins it for the whole server; the other game loses its sidebar. |
| L4 | Mission enemy AI targets the nearest player within 64 blocks, any mode. | `mob_ai.py` | Only a problem if two arenas are closer than 64 blocks. |
| L5 | Double join guards only check the mode being joined. | `helpers/lifecycle.py` (`late_join_flow_lines`) | A player can be in a match and a zombies run at once. |
| L6 | Out-of-bounds markers share one tag, `mgs.oob_point`, read by the match and mission ticks. | `core/spawning.py`, `multiplayer/game/tick.py`, `missions/game/tick.py` | A player within 5 blocks of another mode's out-of-bounds marker dies. |

### Already isolated

- Each mode's own per-player objectives (`mp.*`, `mi.*`, `zb.*`) and fake players (`#mp_*`, `#mi_*`, `#zb_*`).
- XP listeners check both the mode state and the player's `in_game` (`multiplayer/xp.py`, `missions/xp.py`, `zombies/xp.py`).
- Simulated deaths route by `in_game` (`main/damage.py`).
- A player is in one team at a time, and each mode has its own teams: `mgs.red`, `mgs.blue` and `mgs.ffa` (gold) for matches, `mgs.missions` (aqua), `mgs.zombies` (yellow). Their colors differ, so a sidebar shown per team color stays in its mode.
- Post effects are per player.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Three games run side by side without breaking each other (Priority: P1)

A Zombies run is at round 12, a Team Deathmatch starts on another map, and a mission runs elsewhere.
The match ends, then the mission ends. The zombies run is untouched: same map, same bounds, regen and
effects still on, nobody kicked.

**Independent Test**: Start Zombies, then Multiplayer, then Missions, each with one player. Stop them
in the reverse order, then in another order. After each stop, the remaining games play on normally.

**Acceptance Scenarios**:

1. **Given** three games running, **When** any one stops, **Then** only its own entities are removed (B1).
2. **Given** zombies running, **When** a match starts on another map, **Then** zombies bounds and base still apply to zombies players (B2).
3. **Given** a match running, **When** zombies starts, **Then** match players stay in the match (B3).
4. **Given** a match active, **When** a zombies player kills a zombie, **Then** no match score changes (B4).
5. **Given** two modes running, **When** one stops, **Then** the other keeps custom regen, stamina, hurt effects and post effects (B5, B6).
6. **Given** two modes running, **When** one stops, **Then** gamerules match what the remaining mode needs (B7).
7. **Given** a respawn timer running in one mode, **When** another mode starts, **Then** the timer is unaffected (B8).

---

### User Story 2 - Each game's messages and sounds reach only its players (Priority: P2)

**Acceptance Scenarios**:

1. **Given** three games, **When** any game broadcasts a round, win, objective or admin message, title or sound, **Then** only its players and its spectators receive it (L1).
2. **Given** a match running, **When** a zombies player looks at the sidebar, **Then** they do not see the match's sidebar (L3).

---

### User Story 3 - A player is in one game at a time (Priority: P2)

**Acceptance Scenarios**:

1. **Given** a player in any game, **When** they try to join another mode, **Then** they are refused with the game they are in (L5).

### Edge Cases

- Players outside any game (lobby, spectators, operators) receive no game messages, except the server-wide announcements listed in FR-007.
- An operator running admin commands on a game is told the result even if not in it.
- A player leaving one game and joining another in the same tick.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Each mode MUST tag its entities with a mode tag (`mgs.multiplayer_entity`, `mgs.missions_entity`, `mgs.zombies_entity`), and each stop MUST only kill its own. Dropped guns carry no mode tag and expire on their own timer.
- **FR-002**: Map base and bounds MUST be stored per mode (`#<mode>_base_*`, `#<mode>_bound_*`), and each entry point of a mode (`game_tick`, `preload_complete`, `stop`) MUST copy them into the working `#gm_base_*` and `#bound_*` first (`shared/use_map_frame`).
- **FR-003**: No mode MUST write another mode's `in_game` objective.
- **FR-004**: Every `signals/on_kill` and `signals/damage` listener MUST check the acting player's `in_game` for its mode, in addition to the mode state.
- **FR-005**: `#any_game_active` MUST be derived (any of the three modes active), not set and cleared by each mode.
- **FR-006**: Stop cleanup (`fx_reset`, stamina, hunger, attributes, gamemode) MUST target only the stopping mode's players.
- **FR-007**: Broadcasts MUST target the mode's players, and its spectators where it has them. Join announcements stay on `@a`; any other server-wide announcement (game start, game end) MUST be listed in the code.
- **FR-008**: Gamerules MUST be set to the value needed by the modes still running: a stop restores a global default only when no other mode is active. Zombies time of day follows the clock of its map's dimension (FR-012).
- **FR-009**: Shared respawn objectives (`mp.death_count`, `mp.spectate_timer`) MUST only be reset for the mode's players.
- **FR-010**: Joining any mode MUST be refused while the player is in another one.
- **FR-011**: The sidebar MUST be shown per team color (`sidebar.team.<color>`): red, blue and gold for matches, yellow for zombies.
- **FR-013**: `shared/maps/call_script_at_base` MUST take the calling mode, place the script at that mode's base, and every map script MUST check that mode before running.
- **FR-014**: Out-of-bounds markers MUST carry their mode tag, and each mode MUST only check its own.
- **FR-012**: A map MUST carry the dimension it is in (`dimension` in its data, recorded by the map editor on save, overworld when absent), for every mode. Each entry point of a mode (`shared/enter_map`, `MAP_ENTRIES` in `core/commands.py`) MUST run in that dimension, so summons, teleports and forceloads land there. Zombies sets and pauses the clock of that dimension (`time set`, `time pause`), so a map in `mgs:zombies`, which has its own clock, keeps the overworld's time running.
- **FR-015**: A player whose game ends MUST return to the lobby set from the config menu (position, rotation and dimension), when one is set.

### Key Entities

- **Mode tag**: one entity tag per mode, plus `gm_entity` for all.
- **Mode player selector**: `@a[scores={mgs.<mode>.in_game=1}]`, the unit every broadcast and reset uses.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The independent test of US1 passes in every stop order with no visible effect on the remaining games.
- **SC-002**: `grep` for `@a ` without a selector in `src/functional/{multiplayer,missions,zombies}` returns only the documented server-wide announcements.
- **SC-003**: A zombies kill during a match changes no `mp.*` score.

## Assumptions

- One game per mode at a time is enforced by the existing start guards and stays so.
- Progression, XP totals and achievements may stay shared across modes.
- Multiplayer and Missions arenas share the overworld and are far enough apart (64+ blocks) that vanilla AI and sounds do not cross; maps are not checked for it. Zombies leaves the overworld with FR-012, which removes L4 and positional sound leaks for it, but not `tellraw`, scores, gamerules or entity sweeps, which are server-wide whatever the dimension.
- The map editor is not used during games and is out of scope.
