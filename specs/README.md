# Specs

One directory per feature, in the Spec Kit layout (`spec.md` -> `plan.md` -> `tasks.md`).

| Feature | State |
|---|---|
| [001-shader-migration-263](001-shader-migration-263/) | Ported to `/posteffect` and verified in game; Iris checks open in [verification.md](001-shader-migration-263/verification.md) |
| [002-zombies-save-load](002-zombies-save-load/) | Specced only |
| [003-zombie-special-types](003-zombie-special-types/) | Stubs in `zombies/game/round/enemies.py` fall through to `types/normal` |
| [004-multiplayer-kill-cam](004-multiplayer-kill-cam/) | Design sketch only |
| [006-weapon-fire-modes-tacticals](006-weapon-fire-modes-tacticals/) | Two known gaps (`firing/sound.py`, `stats/weapons/grenades.py`) |
| [007-xp-advancements](007-xp-advancements/) | Built (`src/functional/progression/advancements`) |

Working on one of these: run `/speckit-tasks` to regenerate its task list from the current code,
or `/speckit-converge` to have the remaining work appended after a partial implementation.

Not tracked here on purpose: the legacy MGS 4.2 crafting system, which the root README calls out as dropped, not deferred.
Inbox items without a shape yet get `/speckit-specify` when they get one.

# Inbox (quick notes - dump anything here, unorganized "basic" format is fine)
- A day in 2027: Add this map https://www.planetminecraft.com/project/black-ops-ii-mob-of-the-dead-minecraft-in-2013/
- bs.entity.interaction to remove: not used?
- hud rouge quand peu de vie
- Demolition: "Sides swapped" it didn't swapped.
- Multiplayer: better armor
- Zombies: if mannequin falls out of the map the player isn't killed for Out of Bounds
- Zombies: when shooting 
- Multiplayer: when a player dies, spawn a mannequin with the same equipment and selected item and kill it at once, for a death animation
- Multiplayer: bonus streaks
