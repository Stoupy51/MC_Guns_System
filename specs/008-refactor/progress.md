| Lot | Delta | Commit | Verification and notes |
|---|---|---|---|
| 0, audit and plan | +0 / -0 outside `specs/008-refactor/` | see `git log` | measurements in `audit.md`; scripts in `.refactor/audit/` (ignored, local to the container) |
| 1, safety net: `scripts/verify.py` rewritten, `scripts/pyrightconfig.json` deleted | see commit | see `git log` | `check` on an unchanged build: empty; comment-only edit: empty; injected bad command: caught by `check` and `server`; `validate`: 1,617 functions parse with mecha 26.3, 0 errors, 40 unreachable (the audit's 37 functions, `input/any`, `zombies/powerup_drop`, `creative_loot_table`); `server`: 26.3 server + libraries from the committed merged zip, start and `/reload`, 0 datapack errors; ruff, pyright strict, complexipy, `stouputils check` clean on the script |

## Next step

Lot 2 (dead functions and data). Baseline: `.refactor/baseline` from `refactor/all` before lot 2. Server test: `python scripts/verify.py server --java $PWD/.refactor/server/jre/bin/java` (Temurin 25 and the 26.3 `server.jar` sit in `.refactor/server/`; fetch them again from api.adoptium.net and piston-data.mojang.com in a new container).

After any build in a Linux container, the 312 media files of `build/` stored as symlinks (mode 120000) show as modified: never commit them, run `git ls-files -s build | awk '$1=="120000"{print $4}' | xargs git update-index --assume-unchanged`.

The build cannot download Smithed Actionbar here (github.com pages answer 403, raw.githubusercontent.com works), so `load/check_dependencies` and `load/valid_dependencies` lose 2 lines each: never commit them.
