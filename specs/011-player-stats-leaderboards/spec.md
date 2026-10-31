# Feature Specification: Player Stats, Leaderboards, Zombies Knife Camos and Mystery Box Pools

**Feature Branch**: `011-player-stats-leaderboards`

**Created**: 2026-10-31

**Status**: Built, P1 to P4; see [plan.md](plan.md) for what was tested. Decisions settled with the author on 2026-10-31; [plan.md](plan.md) splits the work into P1 to P4.

Leaderboards are inspired by the Switch project (`../Switch/src/datapack/stats/`, `player/stats_storage.py`, `player/username_change.py`): the storage layout and the username change handling are reused in spirit, its full re-sort on every update is not.

## Goals

1. Every player stat recorded, per mode (Zombies, Multiplayer, Missions), viewable for oneself from Quick Actions and for any known player, online or not.
2. Leaderboards: best round per Zombies map (filtered by player count), best time per Missions map, Multiplayer level, Zombies level. Shown in dialogs and in `text_display` holograms placed with the map editor.
3. Zombies knife camos unlocked by Zombies level, picked in Quick Actions.
4. The Quick Actions key opens the same menu as `/trigger mgs.player.config set 1`.
5. The mystery box pool is configurable through storage and dialog, globally and per map.

## Constraints

- Datapack performance (skill `datapack-optimization`): nothing in this feature runs every tick. Increments are score operations at the existing award sites; storage writes happen only at login and at the end of a game; holograms check for nearby players once a second.
- No legacy path kept in parallel (the mystery box `ensure_default_pool` rewrite is replaced, not doubled).
- Existing player data keeps working: the snapshot is backfilled from the scores players already have. Per map records start empty (accepted: the project is in development).
- Every phase closes on `scripts/verify.py validate`, `lint`, `server` and an in-game test on a local server driven over RCON.

## Identity and username changes

Scoreboard holders of players are their names, so today a renamed player silently loses every `mgs.*` score, including levels, challenge counters and `bs.id` (which owns their custom loadouts). Switch handles this; this feature does the same.

- The key of a player is their UUID. Its form is the int array rendered by a macro, `[I;a,b,c,d]`, used as a quoted compound key: `players."[I;a,b,c,d]"`. A dashed UUID string has no native source in commands and would need a hex conversion per login. P1 starts by checking in game that a macro writes and reads such a key (the `;`, brackets and minus signs inside double quotes).
- The name is read at login with the existing `mgs:get_username` loot table probe (`players/append_self`).
- At login (`custom:leave_game` counter, like `mgs.zb.rejoins`): if `players."<uuid>".name` differs from the current name, every persistent per-player objective is copied from the old name to the new one, then the old holder is reset, and `name` is updated. The list of persistent objectives is one Python constant, so nothing is forgotten when an objective is added.
- A case-only rename (`Steve` to `steve`) is a different holder for scores; Switch kicks the player there. Here the copy works the same way since holders are distinct strings; only the test must cover it.
- Disconnection is not an event a datapack can run commands on. A player who leaves keeps their scores (name-keyed scores stay readable while offline), and the snapshot catches up at the end of the game they left (the roster is written by name, offline included) or at their next login.

### Storage shape: one compound per player versus a list

| | `players."<uuid>": {name, ...}` | `players: [{uuid, name, ...}]` |
|---|---|---|
| Read one player | Direct path, no scan | `[{uuid:"..."}]` filter scans the list |
| Write at game end | Direct path per roster player | Filter scan per player |
| Rename | One `name` field | One `name` field |
| Iterate every player | Not possible by index | Natural |

Decision: one compound per player. The only iteration needed (the paginated list of known players) walks `known`, a list of UUIDs appended once at a player's first login and never rewritten, and resolves each name with a macro lookup; ten lookups per page. It does not depend on the leaderboards, which come last.

Leaderboard entries store the UUID only. The displayed name is resolved when a dialog or a hologram is built, so a rename touches one field.

## Data model

```
mgs:stats
	known: ["<uuid>", ...]
	players."<uuid>": {
		name: "Steve",
		zb: {games, rounds, best_round, kills, headshots, downs, deaths, revives, points_earned, points_spent, doors, boxes, wallbuys, perks, pap, traps, powerups, barricades, power, time},
		mp: {games, wins, losses, kills, deaths, headshots, captures, plants, defuses, objectives, time, modes: {"<gamemode>": {games, wins}}},
		mi: {games, completed, kills, headshots, deaths, time},
		level: {mp, zb},
		records: {zb: {"<map_id>": {"<player_count>": round}}, mi: {"<map_id>": ticks}}
	}
	leaderboards: {
		level_mp: [{uuid, value, xp}],
		level_zb: [{uuid, value, xp}],
		zb_map: {"<map_id>": {"all": [{uuid, value, players}], "1": [...], "2": [...], "<n>": [...]}},
		mi_map: {"<map_id>": [{uuid, value, players}]}
	}
```

- K/D, win rate and points shown in hundreds are computed when displayed, never stored.
- `zb_map` keeps each player's best per player count, plus an `all` list with their best whatever the count. A bucket exists once a game with that count ended.
- Missions times are in ticks, from `#mi_timer`, sorted ascending; an entry carries the player count for display.
- Level leaderboards break ties on banked XP (`xp_total`).

## Stats

Every value is a score first; the snapshot copies it. Existing challenge counters are reused when their meaning is exactly the stat's:

| Stat | Objective |
|---|---|
| Zombies kills, headshots, revives, perks, pap, best round | `mgs.adv.zb.kills`, `headshots`, `revives`, `perks`, `pap`, `best_round` |
| Zombies points spent | `mgs.adv.zb.spending` (unit is 100 points, displayed x100) |
| Multiplayer kills, headshots, wins, objectives | `mgs.adv.mp.kills`, `headshots`, `wins`, `objectives` |
| Missions kills, completed | `mgs.adv.mi.kills`, `completed` |
| Levels | `mgs.mp.xp_level`, `mgs.zb.xp_level` |

`mgs.adv.zb.box` counts weapons collected off the box; boxes opened (paid pulls) is a new counter.

New objectives, `mgs.st.<mode>.<stat>`, fed at the site that already pays the matching XP award when there is one:

- `mgs.st.zb.games`, `rounds`, `downs`, `deaths`, `points_earned`, `doors`, `boxes`, `wallbuys`, `traps`, `powerups`, `barricades`, `power`, `time`
- `mgs.st.mp.games`, `losses`, `deaths`, `captures`, `plants`, `defuses`, `time`
- `mgs.st.mp.<gamemode>.games`, `mgs.st.mp.<gamemode>.wins` for each gamemode id of `multiplayer/gamemodes`
- `mgs.st.mi.games`, `headshots`, `deaths`, `time`

`time` is in seconds, added in `progression/tick_player`, which already runs once a second for every player, using the mode's `in_game` flag.

## Leaderboard updates

- Written only at `zombies/game_over`, at the Multiplayer and Missions game ends, and for levels at the same moments plus login.
- Insertion, not re-sort: the player's old entry is removed by UUID, then the list is walked once to find the first entry with a lower value (higher for times), and the entry is inserted there. The index found is the rank.
- Every player is kept, so any player has a rank.
- Zombies game over prints "New record!" with the rank to each roster player who beat their best on that map for that player count.

## Zombies knife camos

| Order | Camo | Zombies level |
|---|---|---|
| 1 | Default | 1 |
| 2 | Autumn | 25 |
| 3 | Galaxy | 50 |
| 4 | Red Polymer | 75 |
| 5 | Gold | 100 |

- Reuses `CAMO_VARIANTS` and the `combat_knife<suffix>` models; the Zombies knife keeps its vanilla reach (`SharedContent.knife_item_snbt`), only its model changes.
- Picked in Quick Actions, stored in a new per-player score `mgs.zb.knife_camo`, applied at game start and on the bleed-out respawn (`zombies/player/inventory/loadout.py`). A locked camo shows its level and cannot be picked.
- Unlock message from `#mgs:progression/on_level_up` when the Zombies level reaches a threshold.
- The Multiplayer knife camo stays free.
- `progression/__init__.py` says "nothing is gated behind a level": the docstring is updated to name the knife camos.
- Rough cost at today's curve (50 XP for level 1, +10 per level, ~2100 XP per hour): level 25 is about 4,000 XP (2 h), 50 about 14,200 XP (7 h), 75 about 30,700 XP (15 h), 100 about 53,500 XP (25 h).

## Quick Actions and menus

- `mgs:open_menu` (the static Quick Actions dialog) keeps one button, which runs `/trigger mgs.player.config set 1`: the same menu as the command. The class menu stays reachable from inside it. The dialog's file name is not frozen; its id may follow its new role.
- Player Settings gains: My Stats, Leaderboards, Players, Knife Camo.
- My Stats and a player's stats: one dialog per mode, paged by mode buttons.
- Players: the known players, paged by 10, each opening their stats.
- Leaderboards: a choice of board, then for Zombies maps a choice of map and player count filter (All, 1, 2, 3, 4 and every count that has entries), top 10 plus the viewer's own rank.

## Holograms

- A new map editor element, `leaderboard`, with fields `board` (`level_mp`, `level_zb`, `zb_map`, `mi_map`), `map_id` (empty: the map it is placed in) and `players` (filter, `all` by default).
- Like Switch: the marker summons its `text_display` when a player is within 24 blocks and kills it when none is, checked once a second; the text is built at summon from the storage, top 10. A leaderboard update kills the displays so they rebuild with fresh data.

## Mystery box pool

What the code does today:

- `zombies/mystery_box/ensure_default_pool` runs at every pull and rewrites `mgs:zombies mystery_box_pool` and `mystery_box_weights` with the defaults, so no other pool can last.
- `weigh_ray_gun` writes the weight at an index computed at build time, which breaks as soon as the pool differs.
- `give_function`: every pool entry carries one, and `collect.py` runs it by macro. Only two values exist, both generated (`default_give/weapon` and `default_give/monkey_bomb`); no map and no other code sets its own. The field is dropped: the collect path picks the give by `weapon_id` (`monkey_bomb` to the tactical slot, everything else through the weapon give).

Decisions:

- The pool format, in storage, is `[{weapon_id, weight}]`; magazine, mag count and consumable come from the catalog at build time. Weight 0 excludes a weapon.
- Global default: `mgs:config zombies.mystery_box_pool`, created with every weapon at its catalog weight when absent (today's behaviour).
- Per map override: `mystery_box_pool` in the Zombies map data, same format. Present, it replaces the global pool for that map.
- The active pool is built once at game start into `mgs:zombies mystery_box_pool` and `mystery_box_weights`; pulls only read it.
- The Ray Gun boost finds the Ray Gun's index by `weapon_id` when the pool is built.
- Admin dialog, from the Zombies setup menu and from the map editor's map settings: every catalog weapon with an on/off toggle and its weight; 0 means excluded. Editing the global pool or the current map's override.

## Admin tools

From `/function mgs:config`: reset one map's Zombies or Missions leaderboard, reset one player's stats (scores and snapshot, levels untouched).

## New frozen identifiers (to approve)

- Storage `mgs:stats`; paths `known`, `players`, `leaderboards`.
- Objectives `mgs.st.*` listed in Stats, `mgs.st.login` (`custom:leave_game`), `mgs.zb.knife_camo`.
- Map editor element `mgs.element.leaderboard` and its saved fields; Zombies map field `mystery_box_pool`.
- `mgs:config zombies.mystery_box_pool`.

## Not to forget

- The rename copy must include `bs.id`, or custom loadouts lose their owner.
- An offline player's scores are read by name through a macro at game end; test it with a player who left mid-game.
- Tests: rename (including case-only), offline player in a roster, first login of a player with old scores (backfill), two players finishing on the same round (rank ties), empty pool after every weapon is excluded (the existing `deny_pool_empty`).
