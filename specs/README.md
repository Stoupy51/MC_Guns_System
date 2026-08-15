# Specs

One directory per feature, in the Spec Kit layout (`spec.md` -> `plan.md` -> `tasks.md`).
Everything here was extracted from the backlog that used to live scattered across the repo:
[TODO_26.3_SHADERS.md](../TODO_26.3_SHADERS.md), [src/functional/zombies/README.md](../src/functional/zombies/README.md),
the "Known WIP" section of the root [README.md](../README.md), and the `# TODO` comments in `src/`.

| Feature | Source of the backlog | State |
|---|---|---|
| [001-shader-migration-263](001-shader-migration-263/) | `TODO_26.3_SHADERS.md` | Researched, nothing ported |
| [002-zombies-save-load](002-zombies-save-load/) | `zombies/README.md` §11 | Specced only |
| [003-zombie-special-types](003-zombie-special-types/) | `round/enemies.py` stubs + `zombies/README.md` §10 | Stubs fall through to `types/normal` |
| [004-multiplayer-kill-cam](004-multiplayer-kill-cam/) | root `README.md`, "Future multiplayer TODO" | Design sketch only |
| [006-weapon-fire-modes-tacticals](006-weapon-fire-modes-tacticals/) | `firing/sound.py`, `stats/weapons/grenades.py` | Two known gaps |

Working on one of these: run `/speckit-tasks` to regenerate its task list from the current code,
or `/speckit-converge` to have the remaining work appended after a partial implementation.

Not tracked here on purpose:

- The legacy MGS 4.2 crafting system. The root README calls it out as dropped, not deferred.
- `zombies/README.md` "Inbox" items (the Mob of the Dead map port, XP advancements). They are one-line
  ideas with no shape yet; `/speckit-specify` them when they get one.
