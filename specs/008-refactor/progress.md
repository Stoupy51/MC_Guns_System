| Lot | Delta | Commit | Verification and notes |
|---|---|---|---|
| 0, audit and plan | +0 / -0 outside `specs/008-refactor/` | see `git log` | measurements in `audit.md`; scripts in `.refactor/audit/` (ignored, local to the container) |

## Next step

Answers recorded in `plan.md`. Open: D2 list review, Double Tap (D3), how to drop `set_items_storage` (D6), network (D10). Then lot 1 (safety net): rewrite `scripts/verify.py`, capture `.refactor/baseline/` from a build of `main` in this container.

After any build in a Linux container, the 312 media files of `build/` stored as symlinks (mode 120000) show as modified: never commit them, run `git ls-files -s build | awk '$1=="120000"{print $4}' | xargs git update-index --assume-unchanged`.
