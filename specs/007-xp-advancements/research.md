# Research: XP Advancements

Every open question from the Technical Context, resolved. Nothing below is left as NEEDS CLARIFICATION.

Schema claims are checked against the game source bundled in this repo under `minecraft_source_code/`,
which is the version `beet.yml` pins (26.2). File and line references are given so they can be re-checked
when the pin moves.

## 1. Vanilla evaluates the thresholds, the pack does not

**Decision**: Every threshold tier is a `minecraft:tick` criterion carrying a `minecraft:entity_scores`
condition. No command grants it.

```json
"criteria": {
  "threshold": {
    "trigger": "minecraft:tick",
    "conditions": {
      "player": [
        {
          "condition": "minecraft:entity_scores",
          "entity": "this",
          "scores": { "mgs.adv.zb.kills": { "min": 2500 } }
        }
      ]
    }
  }
}
```

**Schema check**:

- `minecraft:tick` is `PlayerTrigger`, registered at
  [CriteriaTriggers.java:31](../../minecraft_source_code/net/minecraft/advancements/triggers/CriteriaTriggers.java#L31).
- **`player` is a list.** It holds a `ContextAwarePredicate`, which decodes as a list of loot
  conditions, with an alternative branch that reads a bare `EntityPredicate` (a map keyed by entity
  sub-predicate type) and wraps it. Handing it a single condition object satisfies neither branch: the
  list branch reports the whole object as missed input, and the alternative rejects `condition`,
  `entity` and `scores` as unknown `entity_sub_predicate_type` keys.

  This cost a load cycle to find, because the decompiled dump in `minecraft_source_code/` is **stale for
  this class**: it shows `PlayerTrigger.TriggerInstance` holding `Optional<Holder<LootItemCondition>>`
  and contains no `ContextAwarePredicate` at all, while the running server reports
  `TriggerInstance[player=Optional[ContextAwarePredicate@...]]`. Treat the dump as a strong hint and the
  server log as the authority.
- `minecraft:entity_scores` is `EntityHasScoreCondition`, registered at
  [LootItemConditionTypes.java:15](../../minecraft_source_code/net/minecraft/world/level/storage/loot/predicates/LootItemConditionTypes.java#L15),
  with `scores` an unbounded map of objective name to `IntRange`
  ([EntityHasScoreCondition.java:22](../../minecraft_source_code/net/minecraft/world/level/storage/loot/predicates/EntityHasScoreCondition.java#L22)).
  The pack already uses this condition in its own predicates
  ([traps/setup.py:22](../../src/functional/zombies/objects/traps/setup.py#L22)), so the shape is proven
  in this codebase and not just in the source.

**Rationale**: This is the whole design. It is instant, it needs no scheduling, no polling function and
no `advancement grant`, and it deletes an entire layer that a command-driven version would need: the
per-stat next-threshold companion score, the unlock ladder functions, and the admin resync. The per-event
cost drops to the single command that moves the counter.

It also makes retuning self-healing (FR-011). Vanilla re-evaluates every incomplete advancement, so
lowering a threshold unlocks it on the next tick for everyone who already qualifies, including players
who were offline when the pack changed. Raising one takes nothing back.

**Cost, stated honestly (Constitution IV)**: a `tick` criterion is real per-player, per-tick work on the
server thread. It is a hash lookup and an integer compare in native code, not a command dispatch, and
vanilla unregisters a criterion the moment it completes, so the cost decays to zero as a player finishes
the tree. With 56 tiers the worst case is a brand new player, and it is still orders of magnitude below
one `@e` scan. The pack itself adds no per-tick function at all.

**Alternatives considered**:

- *`advancement grant` from a companion "next threshold" score*: one comparison per award event and an
  unlock ladder per chain. Strictly more pack-side work, more generated functions, more state that can
  desync, and it needs an admin resync after every retune. Rejected in favour of letting the engine do it.
- *A periodic sweep over `@a`*: adds a pack function running forever, and is not instant.

## 2. Where lifetime counters get fed from

**Decision**: Instrument `progression/{side}/award_{key}`, the generated per-award functions in
[curve.py:85](../../src/functional/progression/curve.py#L85). Missions, which grants no XP today, is fed
from `missions/victory` instead.

**Rationale**: Every one of the 29 award rows already funnels through its own generated function, and
that function always runs with `@s` as the earning player. `Xp.give` exists precisely so that no call
site names an amount, which means no call site has to be touched to also name a counter. A stat bump is
one extra line inside a function the codegen already writes, and the thirty-odd award sites scattered
across gamemodes, machines, traps and barricades are covered for free. Fifteen of the 31 award functions
gain exactly one line; the rest are untouched.

**Alternatives considered**:

- *New hooks at each event site*: 30 new edits, 30 new things to forget when a gamemode is added.
- *Vanilla criteria such as `minecraft:player_killed_entity`*: does not cover trap kills, Nuke kills,
  revives, perks, doors or anything else the pack invented, and would double-count against the pack's own
  kill accounting.

## 3. Counters the pack already keeps

**Decision**: The two `level` chains read `mgs.mp.xp_level` and `mgs.zb.xp_level` directly. No new stat,
no new objective, and no subscription to `#mgs:progression/on_level_up`.

**Rationale**: FR-013. Those scores already exist, are already permanent, and are already the number the
challenge is about. Mirroring them into `mgs.adv.*` would be a second copy to keep in sync for no gain.
This is a direct consequence of vanilla doing the evaluation: a command-driven design would have needed
the level-up signal to know when to check, and the score-condition design does not need to know.

`xp_level` is a cache that `recompute` can move downward after a retune. An already unlocked tier stays
unlocked, which is the intended behaviour anyway.

## 4. Counting events that are not worth one

**Decision**: A stat declares its source as a `<holder> <objective>` pair and one of three kinds:

| Kind | Command shape | Used by |
|---|---|---|
| Count by one | `scoreboard players add @s <obj> 1` | Revives, perks, plants, defuses, box pulls, wins |
| Count by a score | `scoreboard players operation @s <obj> += <src>` | Zombies kills (`#zb_kills_delta mgs.data`), points spent (`#xp_gain mgs.data`), mission kills (`@s mgs.mi.kills`) |
| High-water mark | `scoreboard players operation @s <obj> > <src>` | Deepest round |

**Rationale**: The two `scaled=True` Zombies award rows already carry their real count in a score at the
moment the award function runs, so the counter reads the same score the XP amount was computed from.
Expressing the source as a full holder-and-objective pair rather than a bare fake player is what lets the
Missions branch read `@s mgs.mi.kills` with the same machinery.

`scoreboard players operation ... >` is vanilla's max operator, so a high-water mark is one command with
no branch.

**Alternatives considered**:

- *Counting scaled awards as one event*: would make "kills" mean "ticks on which at least one kill was
  credited", which is a different and useless number.
- *Deriving deepest round from `round_survived` payouts*: recoverable by division, but fragile the moment
  `ROUND_XP` is retuned.

## 5. The challenges a score cannot express

**Decision**: A small set of event challenges use `{"trigger": "minecraft:impossible"}` and are granted
by one command at the site that already detects the moment. Three of them, one per branch.

| Id | Moment | Site | Why a score cannot do it |
|---|---|---|---|
| `mp/flawless` | Win a match without dying | `multiplayer/xp/on_game_end` | `mgs.mp.deaths` is per-match and is zeroed on join and on start, so it reads 0 almost always |
| `mi/flawless` | Complete a mission without dying | `missions/victory` | Same, for `mgs.mi.deaths` |
| `zb/solo_20` | Reach round 20 with nobody else in the game | `zombies/on_round_end` | Needs the round and the roster size at the same instant |

`minecraft:impossible` is registered at
[CriteriaTriggers.java:9](../../minecraft_source_code/net/minecraft/advancements/triggers/CriteriaTriggers.java#L9).
It is the standard way to say "only a command opens this door".

**Rationale**: These are the exception the design makes room for, not the rule. Each is one guarded
`advancement grant` at a function that already runs at exactly the right moment with the right players
selected. Granting an advancement a player already owns is a no-op, so the repeat case needs no guard of
its own.

## 6. One tab, three branches

**Decision**: A single root, `mgs:challenges/root`, with three children that are themselves roots of a
branch: `mgs:challenges/mp/root`, `mgs:challenges/mi/root`, `mgs:challenges/zb/root`. Chains parent onto
their branch root; tier N+1 parents onto tier N.

**Rationale**: The tab count in the Advancement screen is the number of parentless advancements, so one
root is one tab. Three separate roots would be three tabs competing with vanilla's own, which is exactly
what the user does not want. Branch roots give the tree its structure without spending a tab on it.

All four roots use an unconditioned `{"trigger": "minecraft:tick"}` criterion, so they complete on a
player's first tick. Roots pay no XP.

## 6b. Making the whole tree visible

**Decision**: Each chain ends in a sentinel advancement with **no `display` block at all**, auto-granted
by an unconditioned `tick` criterion, parented to the chain's last tier.

**Rationale**: Granting the roots is not enough, and believing it was is the mistake this entry exists to
correct. `AdvancementVisibilityEvaluator` shows an unfinished node only when it or one of its two nearest
ancestors is done
([AdvancementVisibilityEvaluator.java:25-38](../../minecraft_source_code/net/minecraft/server/advancements/AdvancementVisibilityEvaluator.java#L25)),
so on a four-tier chain a fresh player sees tiers 1 and 2 and nothing else. Half the catalog would be
invisible, and a challenge nobody can read is a challenge nobody chases.

The same file gives the fix. `evaluateVisibilityRule` returns `HIDE` for any advancement whose `display`
is absent, so a display-less node is never drawn
([line 16-17](../../minecraft_source_code/net/minecraft/server/advancements/AdvancementVisibilityEvaluator.java#L16)),
while `isSelfOrDescendantDone |= evaluateVisibility(child, ...)` ORs a child's done-ness into its parent
all the way up
([line 51-55](../../minecraft_source_code/net/minecraft/server/advancements/AdvancementVisibilityEvaluator.java#L51)).
One completed, invisible leaf therefore lights up its entire ancestor chain while rendering nothing,
announcing nothing and paying nothing.

Sixteen sentinels, one per chain, at `mgs:challenges/<branch>/<chain>_reveal`. The event challenges need
none: they hang directly off a branch root, well inside the two-ancestor window.

`background` is only read on the true root. It is a plain identifier resolved as `textures/<path>.png`
([ClientAsset.java:19-27](../../minecraft_source_code/net/minecraft/core/ClientAsset.java#L19)), so
`"minecraft:block/polished_deepslate"`, not a full file path.

Frames follow the tier position: `task` early, `goal` second to last on long chains, `challenge` last.
That is vanilla's own visual grammar and costs nothing to honour.

## 7. Versioned or unversioned paths

**Decision**: Advancements live at `mgs:challenges/...` with **no** `v{version}` segment. The
`rewards.function` inside them points at the normal versioned function.

**Rationale**: An advancement identifier is per-player persistent state stored in the world, not in the
pack. Putting the version in the path means every pack update mints a fresh set of identifiers and every
player's unlocks vanish. Worse, under this design vanilla would immediately re-evaluate the new
identifiers against the counters and pay the entire catalog out again.

The reward function reference stays versioned because the advancement JSON is regenerated on every build,
so it always names a function that exists in the pack currently loaded. The existing versioned
advancement in the pack ([menu.py:67](../../src/functional/map_editor/menu.py#L67)) is unaffected by any
of this: it is revoked on the same tick it fires and holds no state.

## 8. Not paying twice

**Decision**: Rely on vanilla. `rewards.function` runs when an advancement transitions to completed, and
a completed advancement's criteria stop being evaluated.

**Rationale**: With the pack no longer granting anything on the threshold path, there is no second code
path that could double-fire. The event challenges re-issue `advancement grant` at most once per match and
vanilla no-ops the repeat.

The one case where a payout does repeat is an operator revoking a challenge whose counter still qualifies.
Vanilla grants it again on the next tick and it pays again. That is the same mechanism that makes
retuning self-healing, so it is accepted and documented rather than guarded against.

**Verification**: Constitution V. Checked in [quickstart.md](quickstart.md) by continuing to earn well
past a crossed threshold and confirming no second payout.

## 9. Feedback: toast, chat, or both

**Decision**: `show_toast: true`, `announce_to_chat: false`, and the pack prints its own line.

**Rationale**: Vanilla's announcement cannot carry the XP amount, and the pack already has a convention
for how an XP-bearing message looks (`Xp.announce` / `Xp.suffix`). Two announcements for one event would
be noise. Top-tier `challenge` unlocks broadcast through `Xp.announce` so the server sees them; every
other tier is a private `tellraw @s`, which is the same split the rest of the progression code uses.

Both fields are optional and default to `true`
([DisplayInfo.java:21-22](../../minecraft_source_code/net/minecraft/advancements/DisplayInfo.java#L21)),
so `announce_to_chat` has to be written out explicitly.

## 10. Paying the XP

**Decision**: One new award row per XP pool, `challenge`, with `scaled=True`. The reward function sets
`#xp_gain` to that tier's payout and calls it.

**Rationale**: FR-006. `Xp.give` already handles the cap, the level check, the level-up feedback and the
bar refresh through `settle`. A scaled row means one row covers all 56 payouts, and `Xp.suffix` reads
`#xp_gain` so the message needs no special case. Writing to `xp_total` directly would duplicate `settle`
and skip the level-up announcement.

Missions tiers use the `mp` pool's row, because Missions pays Multiplayer XP (see the spec's assumptions).

**Ordering note**: `#xp_gain` is set before the `tellraw`, because a score text component resolves when
the command runs.

## 11. Titles, descriptions and icons

**Decision**: Plain `{"text": ...}` components for title and description. Icons are either a vanilla item
id or one of the pack's own weapons.

**Rationale**: `stewbeet.plugins.auto.lang_file` walks every text file in `ctx.data.all()`
([scan.py:139](../../../StewBeet/python_package/stewbeet/core/utils/text_component/scan.py#L139)), and
advancements are in there, so titles and descriptions get folded into the pack's language file exactly
like item names and chat lines.

`icon` is an `ItemStackTemplate`
([DisplayInfo.java:16](../../minecraft_source_code/net/minecraft/advancements/DisplayInfo.java#L16)), so
it carries components as well as an id. Every gun in the pack is a `minecraft:poisonous_potato` wearing a
`minecraft:item_model` ([items.py:58](../../src/config/stats/items.py#L58)), which means an icon can show
the real weapon:

```json
"icon": { "id": "minecraft:poisonous_potato", "components": { "minecraft:item_model": "mgs:m249" } }
```

The catalog writes `icon="m249"` for a pack item and `icon="minecraft:beacon"` for a vanilla one, and the
generator tells them apart by the colon. The pack item path goes through `Item.from_id`, which is strict,
so a mistyped weapon id fails the build rather than rendering as a raw potato in game.

Guns are used where the chain is about shooting (kills, headshots), on both branch roots and on the tab
itself. Objectives, perks, rounds and levels keep vanilla items, because a gun on every node would make
the tree unreadable.

## 12. Balance of the payouts

**Decision**: Ten tiers per chain on a shared XP ladder, with the number written out per row. Standard
chains use `10, 20, 30, 50, 75, 110, 160, 230, 275, 340` (1,300 total); the two `level` chains and
`best_round` use `15, 30, 50, 80, 120, 175, 250, 350, 425, 505` (2,000). Multiplayer pool 10,400, Zombies
pool 13,600.

**Rationale**: SC-003. A Zombies run to round 20 is about 1,580 XP
([awards.py:103](../../src/functional/progression/awards.py#L103)), so that pool is worth about 8.6 runs,
spread across a tail that takes far longer than 8.6 runs to finish. A Multiplayer win is 300 to 400 XP,
so its pool is about thirty matches. No single unlock is worth more than a good match, so challenges
accelerate the curve without replacing it.

The ladder is shared rather than per-chain because sixteen bespoke curves would be sixteen things to
retune and no player would ever notice the difference. It is still written out per row rather than
generated, so a single tier can be nudged without touching the rest.

## 12b. Ten tiers, not four

**Decision**: Every chain is ten tiers.

**Rationale**: Shape, not content. Four-tier chains stacked sixteen deep render as a tall narrow column
that has to be scrolled to read, which is what the first build actually looked like. Ten across turns
each chain into a line read left to right and the tab into something roughly square.

It also fixes the pacing at the bottom. With four tiers the first Zombies kills node wanted 250 kills;
with ten it wants 100, and there are four more nodes before the old first one. A challenge tree is most
useful to a new player, and the old one gave them nothing to hit for an hour.

The cost is 160 rows instead of 53, which is why `Tier` was reduced to threshold, XP and title, with
description, icon and frame derived from the chain. Ten near-identical rows per chain would have been
worse than four verbose ones.
