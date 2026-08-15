# Contracts: XP Advancements

What this feature exposes to the world, to operators, and to the rest of the pack. Everything in the
"stable" column is state stored in the player's world rather than in the pack, so renaming it after
release destroys player progress.

## 1. Advancement identifiers (stable, never versioned)

| Id | Stable | Purpose |
|---|---|---|
| `mgs:challenges/root` | Yes | The one MGS tab |
| `mgs:challenges/<branch>/root` | Yes | Branch sub-root: `mp`, `mi`, `zb` |
| `mgs:challenges/<branch>/<chain>_<n>` | Yes | One threshold tier, `n` starting at 1 |
| `mgs:challenges/<branch>/<key>` | Yes | One event challenge |
| `mgs:challenges/<branch>/<chain>_reveal` | Yes | Invisible sentinel closing a chain |

**Contract**: these ids never gain a `v<version>` segment and are never renamed. A chain may gain tiers
at the end; existing tiers are never renumbered. Removing a chain orphans the unlock in every world that
already has it, which is acceptable only as a deliberate, documented removal.

### Threshold tier

```json
{
  "parent": "mgs:challenges/zb/kills_1",
  "display": {
    "icon": { "id": "minecraft:iron_axe" },
    "title": { "text": "Exterminator" },
    "description": { "text": "Kill 2,500 zombies" },
    "frame": "task",
    "show_toast": true,
    "announce_to_chat": false
  },
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
  },
  "rewards": { "function": "mgs:v<version>/progression/adv/zb/kills/reward_2" }
}
```

`player` is a **list**. It is a `ContextAwarePredicate`, and a bare condition object there fails to load
the whole advancement (see [research.md](../research.md) §1).

Vanilla owns the unlock. The pack never runs `advancement grant` for a tier, which is what makes retuning
self-healing and what keeps the per-event cost at one command.

### Event challenge

```json
{
  "parent": "mgs:challenges/mi/root",
  "display": { "...": "...", "frame": "challenge" },
  "criteria": { "granted": { "trigger": "minecraft:impossible" } },
  "rewards": { "function": "mgs:v<version>/progression/adv/mi/reward_flawless" }
}
```

Unreachable by design. The only way in is the single `advancement grant` at its site.

### Roots

```json
{ "display": { "...": "...", "background": "minecraft:block/polished_deepslate", "show_toast": false, "announce_to_chat": false },
  "criteria": { "joined": { "trigger": "minecraft:tick" } } }
```

### Reveal sentinel

```json
{ "parent": "mgs:challenges/zb/kills_4",
  "criteria": { "joined": { "trigger": "minecraft:tick" } } }
```

**No `display` key, deliberately.** That is what makes it unrenderable, while its completion still ORs
up the tree and reveals every tier above it. Adding a display to one of these turns it into a visible
node that pays nothing, which is not what any of them are for.

### Roots

Unconditioned, so a root completes on the player's first tick and the branches below it become visible.
`background` is read only on `mgs:challenges/root` and is a plain identifier resolved as
`textures/<path>.png`, not a file path. Branch roots carry `parent: "mgs:challenges/root"`.

**Reward functions are versioned on purpose.** The advancement JSON is regenerated on every build, so the
reference always names a function that exists in the pack currently loaded.

## 2. Scoreboard objectives

| Objective | Type | Owner |
|---|---|---|
| `mgs.adv.<branch>.<key>` | dummy | This feature. 14 of them |
| `mgs.mp.xp_level`, `mgs.zb.xp_level` | dummy | The progression system. Read by the `level` chains, never written here |

**Contract**: the `mgs.adv.` objectives are never reset by any per-match wipe. `multiplayer/start`,
`missions/start` and `zombies/stop` clear their objectives by explicit name, so these are safe by
construction, and any future wipe-by-prefix would break that guarantee.

An operator setting a counter by hand is supported and is how the quickstart tests thresholds. Setting a
counter *down* does not revoke anything: XP already paid is never taken back.

## 3. Operating the feature

There are no admin functions. Retuning is:

1. Edit the catalog.
2. `uv run beet build`.
3. `/reload`.

Vanilla re-evaluates every incomplete advancement, so a lowered threshold unlocks on the next tick for
everyone who already qualifies, including players who were offline when the pack changed. A raised
threshold takes nothing back.

The one behaviour worth knowing: revoking a challenge whose counter still qualifies causes vanilla to
grant it again on the next tick, and it pays again. That is the same self-healing that makes retuning
work, not a bug to route around.

## 4. Published extension point

```
#mgs:progression/on_challenge_unlock
```

Fired as the player who unlocked, with the payload in `storage mgs:signals on_challenge_unlock`:

| Key | Type | Meaning |
|---|---|---|
| `branch` | string | `mp`, `mi` or `zb` |
| `chain` | string | Chain key, or the event challenge key |
| `tier` | int | 1-based tier index, `0` for an event challenge |
| `side` | string | XP pool that was paid: `mp` or `zb` |
| `xp` | int | What it paid |

This mirrors `#mgs:progression/on_level_up` and exists for the same reason: anything that wants to react
to an unlock subscribes instead of editing the reward functions.

## 5. Sites this feature touches

| Site | What is inserted |
|---|---|
| `progression/{side}/award_{key}` | One counter line, in 15 of the 31 generated award functions |
| `#mgs:zombies/on_round_end` | The `best_round` high-water mark and the `zb/solo_20` grant |
| `missions/victory` | The two Missions counters and the `mi/flawless` grant, after `mgs.mi.kills` is computed |
| `multiplayer/xp/on_game_end` | The `mp/flawless` grant, while the winner tag is still set |
| `progression/{side}/init` | Nothing. Roots complete themselves, and no companion score needs seeding |

## 6. Python-side surface

```python
class Advancements:
	@staticmethod
	def stat_lines(side: str) -> dict[str, str]:
		""" Award key -> the extra lines its generated award function must carry. """

	@staticmethod
	def grant(branch: str, key: str, selector: str = "@s", guard: str = "") -> str:
		""" Return the single command granting one event challenge. """
```

`Curve.write_award_functions` gains one parameter taking that dict. It stays ignorant of what a challenge
is; it only knows some awards carry extra lines. That is what keeps the dependency one-way and avoids an
import cycle between `curve.py` and the advancements package.

`Advancements.grant` mirrors `Xp.give`'s signature deliberately, so the three event sites read like every
other award site in the pack.
