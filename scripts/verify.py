""" Build + snapshot + diff harness for the refactor.

The generated output must not drift while the source is refactored. This script builds the
project, snapshots the generated tree to a reference directory outside `build/`, and diffs
later builds against that reference.

Usage:
    python scripts/verify.py baseline     # build, then (re)capture the reference snapshot
    python scripts/verify.py check        # build, diff against the reference, lint, report
    python scripts/verify.py check --diff # ... and print unified diffs of every changed file
    python scripts/verify.py metrics      # print the metrics table for the current build only

`check` exits non-zero when the output differs, when ruff fails, or when pyright fails, so it
can gate a commit. An intentional diff is acknowledged by re-running `baseline`.
"""

import argparse
import filecmp
import json
import shutil
import subprocess
import sys
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parent.parent
BUILD: Path = ROOT / "build"
SNAPSHOT: Path = ROOT / ".refactor" / "baseline"
METRICS_FILE: str = "metrics.json"

# Only these subtrees are snapshotted: the zips are rebuilt archives (large, and redundant with
# the trees they contain), and `sha1_hashes.json` is derived from them.
SNAPSHOT_TREES: tuple[str, ...] = ("datapack", "resource_pack")

# Binary assets are compared by content but never diffed as text.
TEXT_SUFFIXES: frozenset[str] = frozenset({".mcfunction", ".json", ".mcmeta", ".txt", ".fsh", ".vsh"})


@dataclass(frozen=True, slots=True, kw_only=True)
class Metrics:
    """ The numbers the refactor is measured against. """

    python_files: int
    python_loc: int
    mcfunction_files: int
    mcfunction_command_lines: int
    mcfunction_total_lines: int
    datapack_json_files: int
    resource_pack_json_files: int
    datapack_bytes: int
    resource_pack_bytes: int
    model_source_files: int
    model_source_bytes: int


def _walk(root: Path) -> Iterator[Path]:
    """ Yield every file under `root`, recursively. """
    for path in root.rglob("*"):
        if path.is_file():
            yield path


def _rel_files(root: Path) -> dict[str, Path]:
    """ Map POSIX-style relative path -> absolute path for every file under `root`. """
    return {path.relative_to(root).as_posix(): path for path in _walk(root)}


def collect_metrics() -> Metrics:
    """ Measure the current source tree and the current contents of `build/`. """
    py_files: list[Path] = [p for p in (ROOT / "src").rglob("*.py") if "__pycache__" not in p.parts]
    py_loc: int = sum(len(p.read_text(encoding="utf-8").splitlines()) for p in py_files)

    datapack: Path = BUILD / "datapack"
    resource_pack: Path = BUILD / "resource_pack"
    mcfunctions: list[Path] = list(datapack.rglob("*.mcfunction"))

    command_lines: int = 0
    total_lines: int = 0
    for path in mcfunctions:
        for line in path.read_text(encoding="utf-8").splitlines():
            total_lines += 1
            stripped: str = line.strip()
            if stripped and not stripped.startswith("#"):
                command_lines += 1

    models: Path = ROOT / "src" / "database" / "models"
    model_files: list[Path] = list(models.glob("*.json"))

    return Metrics(
        python_files=len(py_files),
        python_loc=py_loc,
        mcfunction_files=len(mcfunctions),
        mcfunction_command_lines=command_lines,
        mcfunction_total_lines=total_lines,
        datapack_json_files=len(list(datapack.rglob("*.json"))),
        resource_pack_json_files=len(list(resource_pack.rglob("*.json"))),
        datapack_bytes=sum(p.stat().st_size for p in _walk(datapack)),
        resource_pack_bytes=sum(p.stat().st_size for p in _walk(resource_pack)),
        model_source_files=len(model_files),
        model_source_bytes=sum(p.stat().st_size for p in model_files),
    )


def build() -> None:
    """ Run the stewbeet build, failing loudly if it does. """
    print("→ building (stewbeet)…", flush=True)
    result = subprocess.run("stewbeet", cwd=ROOT, shell=True)
    if result.returncode != 0:
        sys.exit(f"build failed (exit {result.returncode})")


def capture_baseline() -> None:
    """ Replace the reference snapshot with the current build output. """
    if SNAPSHOT.exists():
        shutil.rmtree(SNAPSHOT)
    SNAPSHOT.mkdir(parents=True)
    for tree in SNAPSHOT_TREES:
        shutil.copytree(BUILD / tree, SNAPSHOT / tree)
    metrics: Metrics = collect_metrics()
    (SNAPSHOT / METRICS_FILE).write_text(json.dumps(asdict(metrics), indent=2), encoding="utf-8")
    print(f"→ baseline captured at {SNAPSHOT}")
    print_metrics(metrics)


def print_metrics(metrics: Metrics, previous: Metrics | None = None) -> None:
    """ Print the metrics table, with deltas against `previous` when given. """
    print("\n  metric                     value        delta")
    print("  " + "-" * 46)
    for field, value in asdict(metrics).items():
        delta: str = ""
        if previous is not None:
            diff: int = value - getattr(previous, field)
            delta = f"{diff:+d}" if diff else "="
        print(f"  {field:<24} {value:>10}  {delta:>10}")
    print()


def compare_trees() -> tuple[list[str], list[str], list[str]]:
    """ Return (added, removed, changed) relative paths between the snapshot and the build. """
    added: list[str] = []
    removed: list[str] = []
    changed: list[str] = []
    for tree in SNAPSHOT_TREES:
        old: dict[str, Path] = _rel_files(SNAPSHOT / tree)
        new: dict[str, Path] = _rel_files(BUILD / tree)
        added += [f"{tree}/{k}" for k in sorted(new.keys() - old.keys())]
        removed += [f"{tree}/{k}" for k in sorted(old.keys() - new.keys())]
        for key in sorted(old.keys() & new.keys()):
            if not filecmp.cmp(old[key], new[key], shallow=False):
                changed.append(f"{tree}/{key}")
    return added, removed, changed


def print_diffs(changed: list[str]) -> None:
    """ Print a unified diff for every changed text file. """
    import difflib

    for rel in changed:
        tree, _, inner = rel.partition("/")
        old_path: Path = SNAPSHOT / tree / inner
        new_path: Path = BUILD / tree / inner
        if old_path.suffix not in TEXT_SUFFIXES:
            print(f"\n--- {rel}: binary, {old_path.stat().st_size} -> {new_path.stat().st_size} bytes")
            continue
        diff = difflib.unified_diff(
            old_path.read_text(encoding="utf-8").splitlines(),
            new_path.read_text(encoding="utf-8").splitlines(),
            fromfile=f"baseline/{rel}",
            tofile=f"build/{rel}",
            lineterm="",
        )
        print("\n".join(diff))


def run_lint() -> bool:
    """ Run ruff and pyright (strict). Return True when both are clean. """
    ok: bool = True
    print("→ ruff…", flush=True)
    ruff = subprocess.run(
        ["ruff", "check", "src", "--config", "../stouputils/pyproject.toml"], cwd=ROOT, shell=True
    )
    ok &= ruff.returncode == 0
    print("→ pyright (strict)…", flush=True)
    pyright = subprocess.run(["pyright", "-p", "scripts/pyrightconfig.json"], cwd=ROOT, shell=True)
    ok &= pyright.returncode == 0
    return ok


def check(show_diff: bool) -> int:
    """ Build, diff against the baseline, lint, and report. Return the process exit code. """
    if not SNAPSHOT.exists():
        sys.exit(f"no baseline at {SNAPSHOT} — run `python scripts/verify.py baseline` first")

    build()
    added, removed, changed = compare_trees()
    previous = Metrics(**json.loads((SNAPSHOT / METRICS_FILE).read_text(encoding="utf-8")))
    print_metrics(collect_metrics(), previous)

    if not (added or removed or changed):
        print("✅ output is byte-identical to the baseline")
    else:
        print(f"⚠  output differs: {len(added)} added, {len(removed)} removed, {len(changed)} changed")
        for label, group in (("+", added), ("-", removed), ("~", changed)):
            for rel in group[:40]:
                print(f"   {label} {rel}")
            if len(group) > 40:
                print(f"   {label} … and {len(group) - 40} more")
        if show_diff:
            print_diffs(changed)

    lint_ok: bool = run_lint()
    if not lint_ok:
        print("❌ ruff and/or pyright reported problems")
    return 0 if (lint_ok and not (added or removed or changed)) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("baseline", "check", "metrics"))
    parser.add_argument("--diff", action="store_true", help="print unified diffs of changed files")
    args = parser.parse_args()

    match args.command: # type: ignore
        case "baseline":
            build()
            capture_baseline()
            return 0
        case "check":
            return check(args.diff)
        case "metrics":
            print_metrics(collect_metrics())
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
