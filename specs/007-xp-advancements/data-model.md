# Data Model: XP Advancements

Four dataclasses and one enum describe the whole feature. Everything else is generated from them.

## Entities

### `Branch`

One sub-root of the single MGS tab.

| Field | Type | Notes |
|---|---|---|
| `key` | `str` | Path segment and objective segment: `mp`, `mi`, `zb` |
| `side` | `str` | Which XP pool its payouts go into: `mp` or `zb`. Missions is `mp` |
| `title` | `str` | Shown on the branch root |
| `description` | `str` | Shown on the branch root |
| `icon` | `str` | Item id |

`key` and `side` differ only for Missions, and that is the whole reason they are separate fields: the
tree wants three branches, the XP system has two pools.

### `StatKind`

How a stat moves when its event fires. The kind picks the command shape, nothing else.

| Member | Emitted command |
|---|---|
| `COUNT_ONE` | `scoreboard players add @s <obj> 1` |
| `COUNT_SCORE` | `scoreboard players operation @s <obj> += <source>` |
| `MAX_SCORE` | `scoreboard players operation @s <obj> > <source>` |

### `Stat`

The number a chain reads. Either an objective this feature owns, or one the pack already keeps.

| Field | Type | Notes |
|---|---|---|
| `objective` | `str` | Full objective name. Owned stats are `mgs.adv.<branch>.<key>`; borrowed ones name an existing objective such as `mgs.zb.xp_level` |
| `owned` | `bool` | `False` means the pack already declares and maintains it, so no objective is created and no bump is emitted |
| `kind` | `StatKind` | Ignored when `owned` is `False` |
| `sources` | `tuple[str, ...]` | Award keys whose generated function carries the bump. Empty when a dedicated hook feeds it instead |
| `source` | `str` | `<holder> <objective>` read by `COUNT_SCORE` and `MAX_SCORE`, ex: `#zb_kills_delta mgs.data`, `@s mgs.mi.kills`. Empty for `COUNT_ONE` |
| `unit` | `str` | What one point of the counter means, for the description writer. Ex: `1 kill`, `100 points` |
| `note` | `str` | Why this stat exists, for whoever reads the table next |

**Invariants**, asserted at build time so a typo fails the build rather than producing a dead chain:

- Every name in `sources` exists in the award table of the branch's `side`.
- `COUNT_SCORE` and `MAX_SCORE` require a non-empty `source`; `COUNT_ONE` requires an empty one.
- `owned=False` implies empty `sources` and empty `source`: a borrowed objective is never written here.
- An owned stat with empty `sources` must be reachable from exactly one dedicated hook.

### `Tier`

One advancement with a threshold.

| Field | Type | Notes |
|---|---|---|
| `threshold` | `int` | Becomes `{"min": threshold}` in the criterion |
| `xp` | `int` | Paid once, through the `challenge` award row |
| `title` | `str` | Shown in the toast and on the node |
| `description` | `str` | States the requirement in the stat's real unit |
| `icon` | `str` | Item id |
| `frame` | `str` | `task`, `goal` or `challenge` |
| `hidden` | `bool` | Defaults `False`. Reserved for later secret entries |

### `Chain`

One line of a branch.

| Field | Type | Notes |
|---|---|---|
| `key` | `str` | Path segment: `mgs:challenges/<branch>/<key>_<n>` |
| `branch` | `str` | Branch key |
| `stat` | `Stat` | The number this chain reads |
| `tiers` | `tuple[Tier, ...]` | Strictly ascending by `threshold` |

### `EventChallenge`

A challenge with no threshold, granted by the code that detects the moment.

| Field | Type | Notes |
|---|---|---|
| `key` | `str` | Path segment: `mgs:challenges/<branch>/<key>` |
| `branch` | `str` | Branch key |
| `xp` | `int` | Paid once |
| `title`, `description`, `icon` | `str` | As `Tier` |
| `frame` | `str` | Always `challenge` in the first pass |
| `site` | `str` | Where the grant is inserted, for whoever reads the table next |

## Generated state (in the world, not in Python)

| Thing | Lifetime | Meaning |
|---|---|---|
| `mgs.adv.<branch>.<key>` | Permanent | An owned counter |
| `mgs:challenges/...` | Permanent, vanilla | The unlock itself, and the only thing preventing a second payout |

There is deliberately no companion score, no unlock ladder and no resync state. Vanilla evaluating the
criteria is what removes all three.

## Catalog

Titles and descriptions below are the intent; exact wording is a task-time detail. Frames follow the tier
position: `task` early, `goal` second to last on long chains, `challenge` last.

### Tab root: `mgs:challenges/root`

Icon and background only. Criterion is an unconditioned `minecraft:tick`, so it completes on the player's
first tick. No XP.

### Branch `mp` (Multiplayer, pays `mp`): `mgs:challenges/mp/root`

| Chain | Stat | Fed by | Tiers (threshold / XP) |
|---|---|---|---|
| `kills` | `mgs.adv.mp.kills`, count one | award `kill` | 50 / 50, 500 / 150, 2500 / 400, 10000 / 1000 |
| `headshots` | `mgs.adv.mp.headshots`, count one | award `headshot` | 25 / 50, 250 / 200, 1500 / 600 |
| `objectives` | `mgs.adv.mp.objectives`, count one | awards `dom_capture`, `hp_capture`, `bomb_plant`, `bomb_defuse`, `site_destroyed` | 10 / 50, 100 / 200, 500 / 600 |
| `wins` | `mgs.adv.mp.wins`, count one | award `match_win` | 5 / 50, 25 / 200, 100 / 800 |
| `level` | `mgs.mp.xp_level`, borrowed | already maintained | 10 / 100, 25 / 250, 50 / 600, 100 / 1500 |

Event challenge `mp/flawless`, 300 XP: win a match without dying. Granted in
`multiplayer/xp/on_game_end` to winners with `mgs.mp.deaths` at 0.

Branch total: 18 advancements, 7,100 XP.

### Branch `mi` (Missions, pays `mp`): `mgs:challenges/mi/root`

| Chain | Stat | Fed by | Tiers (threshold / XP) |
|---|---|---|---|
| `completed` | `mgs.adv.mi.completed`, count one | hook on `missions/victory` | 1 / 50, 10 / 200, 50 / 600 |
| `kills` | `mgs.adv.mi.kills`, count by `@s mgs.mi.kills` | same hook | 250 / 50, 2500 / 200, 10000 / 600 |

Event challenge `mi/flawless`, 300 XP: complete a mission without dying. Granted in `missions/victory`
for players with `mgs.mi.deaths` at 0.

Branch total: 7 advancements, 2,000 XP into the Multiplayer pool.

Missions is the one branch with no XP awards of its own, so all three hooks land in `missions/victory`,
which already computes `mgs.mi.kills` from the `totalKillCount` delta immediately before its summary
([tick.py:83-86](../../src/functional/missions/game/tick.py#L83)). The counter bumps go after that
computation and before the summary is printed.

### Branch `zb` (Zombies, pays `zb`): `mgs:challenges/zb/root`

| Chain | Stat | Fed by | Tiers (threshold / XP) |
|---|---|---|---|
| `kills` | `mgs.adv.zb.kills`, count by `#zb_kills_delta mgs.data` | award `kill` | 250 / 50, 2500 / 150, 10000 / 400, 50000 / 1200 |
| `headshots` | `mgs.adv.zb.headshots`, count one | award `headshot` | 100 / 50, 1000 / 200, 5000 / 600 |
| `best_round` | `mgs.adv.zb.best_round`, max of the round number | hook on `#mgs:zombies/on_round_end` | 10 / 100, 20 / 250, 30 / 600, 50 / 1500 |
| `revives` | `mgs.adv.zb.revives`, count one | award `revive` | 5 / 50, 25 / 200, 100 / 600 |
| `perks` | `mgs.adv.zb.perks`, count one | award `perk` | 10 / 50, 50 / 200, 200 / 500 |
| `pack_a_punch` | `mgs.adv.zb.pap`, count one | award `pack_a_punch` | 5 / 50, 25 / 200, 100 / 600 |
| `box` | `mgs.adv.zb.box`, count one | award `mystery_box` | 10 / 50, 50 / 200, 200 / 500 |
| `spending` | `mgs.adv.zb.spending`, count by `#xp_gain mgs.data` | award `points_spent` | 500 / 50, 2500 / 200, 10000 / 600 |
| `level` | `mgs.zb.xp_level`, borrowed | already maintained | 10 / 100, 25 / 250, 50 / 600, 100 / 1500 |

Event challenge `zb/solo_20`, 500 XP: reach round 20 with nobody else in the game. Granted on the same
`on_round_end` hook as `best_round`.

Branch total: 31 advancements, 12,100 XP.

The `spending` counter is in units of 100 points, because `points_spent` pays one XP per `POINTS_PER_XP`
and its `#xp_gain` is already that quotient. Its thresholds therefore read as 50,000 / 250,000 /
1,000,000 points, and the descriptions must say points rather than counter units.

### Totals

60 advancement files (56 tiers and event challenges, plus 4 roots). 16 chains, 3 event challenges,
14 new dummy objectives, 2 borrowed objectives.

Award functions that gain one line: 8 on the `mp` side (`kill`, `headshot`, `dom_capture`, `hp_capture`,
`bomb_plant`, `bomb_defuse`, `site_destroyed`, `match_win`) and 7 on the `zb` side (`kill`, `headshot`,
`revive`, `perk`, `pack_a_punch`, `mystery_box`, `points_spent`). The other 16 award functions are
untouched.

## Award table additions

One row per XP pool in [awards.py](../../src/functional/progression/awards.py):

```
XpAward(key="challenge", amount=0, note="Any challenge unlocked; the tier's payout arrives in #xp_gain", scaled=True)
```

`scaled=True` is what lets a single row cover 56 different payouts, and what makes `Xp.suffix` read
`#xp_gain` instead of a compile-time number.

## Relationships

```
mgs:challenges/root                          the one tab
 └── Branch                                  3, each a sub-root
      ├── Chain                              16 total
      │    ├── Stat                          owned (14) or borrowed (2)
      │    └── Tier[]                        3 or 4, strictly ascending
      └── EventChallenge                     1 per branch

Stat(owned) ──fed by──> award functions listed in `sources`
Stat(owned) ──fed by──> a dedicated hook          (best_round, the Missions pair)
Stat(borrowed) ────────> nothing; the pack already writes it

Tier            ──read by──> its own tick criterion, evaluated by vanilla
EventChallenge  ──granted by──> one command at `site`
both            ──pay──> XP through the branch side's `challenge` award row
```
