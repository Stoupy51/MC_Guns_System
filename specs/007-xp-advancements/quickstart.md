# Quickstart: XP Advancements

The in-game run that proves the feature works. Constitution V: nothing here is done until it has been
exercised in Minecraft at the version pinned in `beet.yml` (26.2).

Counters are plain scoreboards and vanilla evaluates them every tick, so no threshold has to be reached
by playing to it. One `/scoreboard` command and the unlock fires on the next tick. That is the whole
reason this is checkable in a few minutes rather than a few weeks.

## Prerequisites

```powershell
uv run beet build
```

The build copies the datapack and resource pack to the destinations in `beet.yml`. In game:

```
/reload
```

Substitute the pack version from `beet.yml` (`5.1.0` at time of writing) wherever `<v>` appears below.

## 1. One tab, three branches

**Run**: open the Advancement screen (`L`).

**Expect**: exactly **one** MGS tab, not three. Its root is already completed (the roots are
unconditioned `tick` criteria, so they finish on the first tick), the Multiplayer, Missions and Zombies
sub-roots hang off it, and every chain's first tier is visible.

Hover a few entries: titles and descriptions are readable English, not raw translation keys.

**Rules out**: a branch root that lost its `parent` and became a second tab, a mis-parented chain, an
unregistered advancement folder.

Then confirm the localization went through the pack's normal path:

```powershell
Select-String -Path build/resource_pack/assets/minecraft/lang/en_us.json -Pattern "challenges"
```

**Expect**: entries for the challenge titles and descriptions. If they are absent, the display components
were built in a shape `auto.lang_file` does not walk.

## 2. A threshold unlocks itself

```
/scoreboard players set @s mgs.adv.zb.kills 250
```

Do not run anything else. Do not grant anything.

**Expect**, within a tick: the vanilla toast, one chat line naming the challenge and its XP, and the
Zombies level bar moving.

```
/scoreboard players get @s mgs.zb.xp_total
```

**Expect**: risen by exactly that tier's payout.

**Rules out**: the criterion shape being wrong for this version (nothing would ever fire), `#xp_gain`
read before it was set (the message would show the previous award's number), a reward function that
writes `xp_total` directly and skips `settle`, and a double announcement from `announce_to_chat` having
been left at its default of `true`.

## 3. It pays once

```
/scoreboard players add @s mgs.adv.zb.kills 1000
/scoreboard players get @s mgs.zb.xp_total
```

**Expect**: risen only by tier 2's payout when 2,500 is crossed, and by nothing at all while the counter
sits between thresholds. No repeat of the tier-1 message at any point.

## 4. Several tiers cross at once

```
/scoreboard players set @s mgs.adv.zb.kills 60000
```

**Expect**: all four tiers unlock and all four payouts land. Vanilla completes them in the same tick.

**Rules out**: a parent chain that blocks a child from being evaluated before its parent completes.

## 5. Counters move by the real amount

**Scaled**: in a Zombies game, note `mgs.adv.zb.kills`, then trigger a Nuke.

**Expect**: the counter jumps by the number of zombies the Nuke actually killed, not by one.

**Max**: play or force a round advance.

```
/scoreboard players get @s mgs.adv.zb.best_round
```

**Expect**: the round number just cleared. Start a fresh game and clear round 1.

**Expect**: `best_round` unchanged, because it is a high-water mark.

**Borrowed**: grant yourself enough XP to cross Multiplayer level 10.

**Expect**: the Multiplayer `level` chain's first tier unlocks, with no `mgs.adv.mp.level` objective
existing anywhere. The chain reads `mgs.mp.xp_level` directly.

## 6. The event challenges

Play a mission through to victory without dying.

**Expect**: `mi/flawless` unlocks, the Missions `completed` counter rises by one, and the Missions `kills`
counter rises by that mission's kills.

Play another, die once, finish it.

**Expect**: the two counters move again, and `mi/flawless` does not fire a second message. Nothing pays.

Then check the branch really is paying the right pool:

```
/scoreboard players get @s mgs.mp.xp_total
/scoreboard players get @s mgs.zb.xp_total
```

**Expect**: the Multiplayer total moved and the Zombies total did not. Missions pays Multiplayer XP.

## 7. Nothing is wiped by a match

Start and finish a Multiplayer match, a mission, and a Zombies run.

```
/scoreboard players get @s mgs.adv.mp.kills
/scoreboard players get @s mgs.adv.mi.completed
/scoreboard players get @s mgs.adv.zb.kills
```

**Expect**: all three survived. `multiplayer/start`, `missions/start` and `zombies/stop` reset their
objectives by explicit name, so this confirms nothing new was added to those lists by accident.

## 8. A version bump keeps the unlocks

Edit `version` in `beet.yml`, rebuild, `/reload`, open the Advancement screen.

**Expect**: every previously unlocked challenge still unlocked, counters intact, `xp_total` unchanged, and
no flood of toasts.

**Rules out**: the single failure this design exists to prevent. If the tab comes back empty and then
immediately re-pays everything, an advancement path picked up a `v<version>` segment somewhere.

Restore `version` afterwards.

## 9. A retune self-heals, with nothing run by hand

Lower a threshold in the catalog to below a counter you already have. Rebuild, `/reload`.

**Expect**: the tier unlocks within a tick and pays once. **No command is run to make this happen.** If
it needs a nudge, the criterion is not being evaluated and something is granting instead.

Raise a threshold back above a counter for a tier already unlocked. Rebuild, `/reload`.

**Expect**: still unlocked, nothing taken back, no second payout.

## 10. Cost

`F3 + L` for a few seconds during a busy Zombies round, then read the report with
[Misode's analyzer](https://misode.github.io/report/).

**Expect**: no `progression/adv/*` function in the hot list, and none of them present at all except on a
tick where a challenge actually unlocked. The only per-event pack cost is the one counter line living
inside the award functions.

Vanilla's own criterion checking will not show up as a datapack function, because it is not one. To sanity
check that side, compare tick time on a fresh account (56 live criteria) against one that has finished the
tree (none). The gap is the ceiling on what this feature costs the server.
