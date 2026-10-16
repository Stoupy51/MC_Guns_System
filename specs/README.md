# Specs

One directory per feature, in the Spec Kit layout (`spec.md` -> `plan.md` -> `tasks.md`).

| Feature | State |
|---|---|
| [002-zombies-save-load](002-zombies-save-load/) | Suspend and resume (P1) built and played (disconnect, restart, stale player); save slots specced |
| [003-zombie-special-types](003-zombie-special-types/) | Built; T001 and T003 (package move) and the in-game checks open |
| [004-multiplayer-kill-cam](004-multiplayer-kill-cam/) | Specced: final kill chain replayed with mannequins |
| [006-weapon-fire-modes-tacticals](006-weapon-fire-modes-tacticals/) | Built, in-game checks open (T012, T013, T020) |
| [008-original-fire-modes](008-original-fire-modes/) | Built, in-game checks open (T014 to T017) |
| [009-concurrent-modes-isolation](009-concurrent-modes-isolation/) | Built and played with two clients: map dimension, lobby, mgs:zombies dimension; L4 and the tab list open |

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
