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
| `icon` | `str` | Item id. Empty falls back to the chain's icon |
| `description` | `str` | Empty falls back to the chain's template with the threshold filled in |
| `frame` | `str` | Empty derives from position: last is `challenge`, the two before it `goal`, the rest `task` |
| `hidden` | `bool` | Defaults `False`. Reserved for later secret entries |

A chain is ten rows long, so a row spells out only what is genuinely its own: how far along it sits, what
it pays, and what it is called. Writing description, icon and frame on all 160 rows would be ten
near-copies per chain and would bury the three values that actually differ. Deriving the frame also means
a chain cannot end on a `task` by accident.

### `Chain`

One line of a branch. Ten tiers, because four-tier chains stacked sixteen deep made the advancement
screen a tall thin column instead of something read left to right.

| Field | Type | Notes |
|---|---|---|
| `key` | `str` | Path segment: `mgs:challenges/<branch>/<key>_<n>` |
| `branch` | `str` | Branch key |
| `stat` | `Stat` | The number this chain reads |
| `icon` | `str` | Fallback icon for rows that do not name their own |
| `description` | `str` | Fallback template, `{count}` where the threshold goes, ex: `Kill {count} zombies` |
| `tiers` | `tuple[Tier, ...]` | Strictly ascending by `threshold` |

`Chain.icon_of`, `Chain.description_of` and `Chain.frame_of` resolve a row against these. Thresholds are
formatted with thousands separators in descriptions, so no chain writes "Kill 50000 zombies".

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

Sixteen chains of ten. The tables below give each chain's feed and its threshold range; the per-tier
numbers, titles and icons live in `advancements/catalog/`, which is the source of truth and the only
place to retune them.

Every chain uses the same XP ladder, `10, 20, 30, 50, 75, 110, 160, 230, 275, 340`, summing to 1,300. The
three marquee chains (both `level` chains and `best_round`) use a heavier one,
`15, 30, 50, 80, 120, 175, 250, 350, 425, 505`, summing to 2,000.

### Tab root: `mgs:challenges/root`

Icon and background only. Criterion is an unconditioned `minecraft:tick`, so it completes on the player's
first tick. No XP.

### Branch `mp` (Multiplayer, pays `mp`): `mgs:challenges/mp/root`

| Chain | Stat | Fed by | Thresholds | XP |
|---|---|---|---|---|
| `kills` | `mgs.adv.mp.kills`, count one | award `kill` | 25 to 10,000 | 1,300 |
| `headshots` | `mgs.adv.mp.headshots`, count one | award `headshot` | 10 to 5,000 | 1,300 |
| `objectives` | `mgs.adv.mp.objectives`, count one | awards `dom_capture`, `hp_capture`, `bomb_plant`, `bomb_defuse`, `site_destroyed` | 5 to 1,500 | 1,300 |
| `wins` | `mgs.adv.mp.wins`, count one | award `match_win` | 1 to 150 | 1,300 |
| `level` | `mgs.mp.xp_level`, borrowed | already maintained | 10, 20, 30, 40, 50, 75, 100, 125, 150, 200 | 2,000 |

Event challenge `mp/flawless`, 300 XP: win a match without dying. Granted in
`multiplayer/xp/on_game_end` to winners with `mgs.mp.deaths` at 0.

Branch total: 51 advancements, 7,500 XP.

### Branch `mi` (Missions, pays `mp`): `mgs:challenges/mi/root`

| Chain | Stat | Fed by | Thresholds | XP |
|---|---|---|---|---|
| `completed` | `mgs.adv.mi.completed`, count one | hook on `missions/victory` | 1 to 150 | 1,300 |
| `kills` | `mgs.adv.mi.kills`, count by `@s mgs.mi.kills` | same hook | 100 to 35,000 | 1,300 |

Event challenge `mi/flawless`, 300 XP: complete a mission without dying. Granted in `missions/victory`
for players with `mgs.mi.deaths` at 0.

Branch total: 21 advancements, 2,900 XP into the Multiplayer pool.

Neither counter rides an award function even though missions now has some, because one counts victories
and the other reads the whole mission's kill total in one go. Both land in `missions/victory`, which
computes `mgs.mi.kills` from the `totalKillCount` delta immediately before its summary
([tick.py:83-86](../../src/functional/missions/game/tick.py#L83)).

### Branch `zb` (Zombies, pays `zb`): `mgs:challenges/zb/root`

| Chain | Stat | Fed by | Thresholds | XP |
|---|---|---|---|---|
| `kills` | `mgs.adv.zb.kills`, count by `#zb_kills_delta mgs.data` | award `kill` | 100 to 50,000 | 1,300 |
| `headshots` | `mgs.adv.zb.headshots`, count one | award `headshot` | 50 to 15,000 | 1,300 |
| `best_round` | `mgs.adv.zb.best_round`, max of the round number | hook on `#mgs:zombies/on_round_end` | 5, 10, 15, 20, 25, 30, 35, 40, 50, 60 | 2,000 |
| `revives` | `mgs.adv.zb.revives`, count one | award `revive` | 1 to 150 | 1,300 |
| `perks` | `mgs.adv.zb.perks`, count one | award `perk` | 5 to 500 | 1,300 |
| `pack_a_punch` | `mgs.adv.zb.pap`, count one | award `pack_a_punch` | 1 to 150 | 1,300 |
| `box` | `mgs.adv.zb.box`, count one | award `mystery_box` | 1 to 500 | 1,300 |
| `spending` | `mgs.adv.zb.spending`, count by `#xp_gain mgs.data` | award `points_spent` | 100 to 35,000 | 1,300 |
| `level` | `mgs.zb.xp_level`, borrowed | already maintained | 10, 20, 30, 40, 50, 75, 100, 125, 150, 200 | 2,000 |

Event challenge `zb/solo_run`, 500 XP: reach round 20 with nobody else in the game. Granted on the same
`on_round_end` hook as `best_round`.

Branch total: 91 advancements, 13,600 XP.

The `spending` counter is in units of 100 points, because `points_spent` pays one XP per `POINTS_PER_XP`
and its `#xp_gain` is already that quotient. Its thresholds therefore mean 10,000 to 3,500,000 points,
and every row in that chain writes its description out in points rather than counter units.

### Totals

183 advancement files: 160 tiers, 3 event challenges, 4 roots, and 16 invisible reveal sentinels.
16 chains, 14 new dummy objectives, 2 borrowed objectives.

Pools: 10,400 XP Multiplayer (about 30 matches), 13,600 XP Zombies (about 8.6 round-20 runs).

The sentinels carry no `display`, no rewards and no XP. They exist only so vanilla's visibility rule
shows a whole chain instead of its first two tiers (see [research.md](research.md) §6b), and they live at
`mgs:challenges/<branch>/<chain>_reveal`.

### Icons

`Tier.icon` and `Branch.icon` take either a namespaced vanilla id (`minecraft:beacon`) or one of the
pack's own item ids (`m249`). The generator tells them apart by the colon and resolves a pack id through
`Item.from_id` into its base item plus its `item_model`, so the advancement screen shows the real weapon.
Shooting chains use guns; objectives, perks, rounds and levels keep vanilla items.

Award functions that gain one line: 8 on the `mp` side (`kill`, `headshot`, `dom_capture`, `hp_capture`,
`bomb_plant`, `bomb_defuse`, `site_destroyed`, `match_win`) and 7 on the `zb` side (`kill`, `headshot`,
`revive`, `perk`, `pack_a_punch`, `mystery_box`, `points_spent`). The other 16 award functions are
untouched.

## Award table additions

One `challenge` row per XP pool in [awards.py](../../src/functional/progression/awards.py):

```
XpAward(key="challenge", amount=0, note="Any challenge unlocked; the tier's payout arrives in #xp_gain", scaled=True)
```

`scaled=True` is what lets a single row cover all 163 payouts, and what makes `Xp.suffix` read `#xp_gain`
instead of a compile-time number.

### Missions XP

Missions granted no XP at all before this feature: there is no `Xp.give` anywhere under
`src/functional/missions/`. A Missions branch paying into a mode that never paid would have been half a
feature, so three more rows go into the `mp` table:

| Row | Amount | Where |
|---|---|---|
| `mission_kill` | 3 | `missions/xp/on_kill`, on the shared `signals/on_kill` tag |
| `mission_headshot` | 3 | Same listener, on top of the kill, off the `on_kill` payload |
| `mission_complete` | 50 | `missions/victory`, to everyone still on the roster |

Deliberately **not** reusing `kill` and `headshot`: the Multiplayer kills chain counts the `kill` row and
its nodes say "Kill N players". A mission enemy is not a player, and folding the two together would make
that chain lie.

`mission_complete` prints no line of its own. Its suffix is appended to the per-player line the victory
summary already prints, which is the same rule every other award in the pack follows.

A mission of roughly 60 enemies therefore pays about 230 XP, in the same range as a Multiplayer match.

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
