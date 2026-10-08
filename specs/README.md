# Specs

One directory per feature, in the Spec Kit layout (`spec.md` -> `plan.md` -> `tasks.md`).

| Feature | State |
|---|---|
| [002-zombies-save-load](002-zombies-save-load/) | Specced only |
| [003-zombie-special-types](003-zombie-special-types/) | Stubs in `zombies/game/round/enemies.py` fall through to `types/normal` |
| [004-multiplayer-kill-cam](004-multiplayer-kill-cam/) | Design sketch only |
| [006-weapon-fire-modes-tacticals](006-weapon-fire-modes-tacticals/) | Two known gaps (`firing/sound.py`, `stats/weapons/grenades.py`) |

Working on one of these: run `/speckit-tasks` to regenerate its task list from the current code,
or `/speckit-converge` to have the remaining work appended after a partial implementation.

Not tracked here on purpose: the legacy MGS 4.2 crafting system, which the root README calls out as dropped, not deferred.
Inbox items without a shape yet get `/speckit-specify` when they get one.

# Inbox (quick notes - dump anything here, unorganized "basic" format is fine)
- A day in 2027: Add this map https://www.planetminecraft.com/project/black-ops-ii-mob-of-the-dead-minecraft-in-2013/
- bs.entity.interaction to remove: not used?
- Demolition: "Sides swapped" it didn't swapped.
- Multiplayer: better armor
- Zombies: if mannequin falls out of the map the player isn't killed for Out of Bounds
- Zombies: when shooting 
- Multiplayer: when a player dies, spawn a mannequin with the same equipment and selected item and kill it at once, for a death animation
- Multiplayer: bonus streaks
- Iris: test a heavy shaderpack (flash bloom, scope, crosshair, hurt), look for banding from grading an already tonemapped image, and re-read Iris `MixinPostChain` on each Iris update (an empty class today)
- Hit indicator: port the font-glyph arc in `weapon/hud/hit_indicator.py` to a `/posteffect` id?
- Muzzle flash seen from another player: `player/fire_weapon` gives every observer within 16 blocks the shooter's post effect, which lights the scene from the observer's camera and draws the spark on the observer's own gun. A post pass only gets `Globals` (camera position, no rotation, no matrices: `PostChain.createPass`), so no baked id can place the shooter on screen. Keep the post effect for the shooter and give observers a `particle flash{color:...}` at the muzzle, plus a `light` block for 2 ticks if the world should light up
