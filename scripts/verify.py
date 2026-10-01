""" Safety net for refactors: the generated pack must not change unless a change is meant.

`baseline` snapshots the build.
`check` diffs a new build against that snapshot, with comments and blank lines ignored.
`validate` parses every function with mecha and finds missing and unreachable resources.
`server` loads the pack in a real server and reloads it.
`lint` runs ruff, pyright and complexipy.
"""
# Imports
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from collections.abc import Iterator
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

from stouputils.typing import JsonDict

# Constants
ROOT: Path = Path(__file__).resolve().parent.parent
BUILD: Path = ROOT / "build"
WORK: Path = ROOT / ".refactor"
BASELINE: Path = WORK / "baseline"
TREES: tuple[str, ...] = ("datapack", "resource_pack")
MINECRAFT: str = "26.3"
ID_TOKEN: re.Pattern[str] = re.compile(r"(?<![\w.\-/:$])(#?)([a-z0-9_.\-]+):([a-z0-9_./\-]*(?:\$\([a-z_0-9]+\)[a-z0-9_./\-]*)*)")
""" A resource id as it appears in commands and JSON, macro placeholders included. """
CALL: re.Pattern[str] = re.compile(r"(?<![\w/])function\s+(#?)([a-z0-9_.\-]+:[a-z0-9_./\-]+)(?![a-z0-9_./\-$(])")
""" A static function or function tag call. """
SERVER_ERROR: re.Pattern[str] = re.compile(r"/(ERROR|WARN)\].*(function|data ?pack|Couldn't|Failed|Unknown|parse)", re.IGNORECASE)

type Key = tuple[str, str]
""" (registry, id), e.g. ("tags/function", "mgs:load"). """


# Classes
@dataclass
class Resource:
	""" A datapack file and the resources it references. """
	registry: str
	text: str
	""" Commands only for a function, raw JSON otherwise. """
	refs: set[Key] = field(default_factory=set[Key])


# Functions
def build() -> None:
	""" Run StewBeet, then remove the folder its livereload plugin makes from the Windows paths of beet.yml. """
	if subprocess.run([str(ROOT / ".venv/bin/stewbeet"), "build"], cwd=ROOT).returncode != 0:
		sys.exit("build failed")
	shutil.rmtree(ROOT / "D:", ignore_errors=True)


def files(root: Path) -> Iterator[tuple[str, Path]]:
	for path in sorted(root.rglob("*")):
		if path.is_file():
			yield path.relative_to(root).as_posix(), path


def commands(text: str) -> list[str]:
	""" Lines a function executes: no comments, no blank lines. """
	return [line.strip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")]


def check(show: bool) -> int:
	""" Diff the current build against the baseline, file by file. """
	changed = [line for tree in TREES for line in diff_tree(tree, show)]
	print("\n".join(changed) or "no difference with the baseline")
	return 1 if changed else 0


def diff_tree(tree: str, show: bool) -> list[str]:
	old = {rel: p for rel, p in files(BASELINE / tree) if not rel.endswith(".map")}
	new = {rel: p for rel, p in files(BUILD / tree) if not rel.endswith(".map")}
	lines = [f"+ {tree}/{rel}" for rel in sorted(new.keys() - old.keys())]
	lines += [f"- {tree}/{rel}" for rel in sorted(old.keys() - new.keys())]
	for rel in sorted(old.keys() & new.keys()):
		if meaning(rel, old[rel]) == meaning(rel, new[rel]):
			continue
		lines.append(f"~ {tree}/{rel}")
		if show and rel.endswith(".mcfunction"):
			before, after = commands(old[rel].read_text(encoding="utf-8")), commands(new[rel].read_text(encoding="utf-8"))
			lines += [f"    - {c}" for c in before if c not in after] + [f"    + {c}" for c in after if c not in before]
	return lines


def meaning(rel: str, path: Path) -> object:
	""" What a file means to the game, so that formatting and comments never show as a difference. """
	if rel.endswith(".mcfunction"):
		return commands(path.read_text(encoding="utf-8"))
	if rel.endswith((".json", ".mcmeta")):
		return json.loads(path.read_text(encoding="utf-8"))
	return hashlib.sha1(path.read_bytes()).hexdigest()


def validate() -> int:
	""" Commands parse, JSON parses, nothing calls a missing function; unreachable resources are listed. """
	errors = parse_errors()
	resources = load_resources(BUILD / "datapack")
	link(resources)
	errors += missing_calls(resources)
	data_kinds = ("function", "predicate", "loot_table", "item_modifier")
	unreachable = sorted(k[1] for k in resources.keys() - reachable(resources) if k[0] in data_kinds)
	print(f"{len(unreachable)} unreachable functions and data files:", *unreachable, sep="\n  ")
	print(f"{len(errors)} errors", *errors, sep="\n  ")
	return 1 if errors else 0


def parse_errors() -> list[str]:
	with ProcessPoolExecutor() as pool:
		errors = [e for e in pool.map(parse_function, sorted((BUILD / "datapack").rglob("*.mcfunction")), chunksize=32) if e]
	for path in BUILD.glob("*pack/**/*.json"):
		try:
			json.loads(path.read_text(encoding="utf-8"))
		except json.JSONDecodeError as exc:
			errors.append(f"{path.relative_to(BUILD)}: {exc}")
	return errors


def parse_function(path: Path) -> str:
	""" Empty when mecha parses the function with the target version's command tree, else the error. """
	from beet import Function
	from mecha import Mecha
	from mecha.diagnostic import DiagnosticError, DiagnosticErrorSummary
	try:
		Mecha(version=MINECRAFT).parse(Function(path.read_text(encoding="utf-8")))
	except (DiagnosticError, DiagnosticErrorSummary) as exc:
		return f"{path.relative_to(BUILD)}: {str(exc).splitlines()[0]}"
	return ""


def load_resources(datapack: Path) -> dict[Key, Resource]:
	""" Every function, JSON resource and tag of the datapack. """
	resources: dict[Key, Resource] = {}
	for rel, path in files(datapack / "data"):
		ns, registry, *rest = rel.split("/")
		if registry == "tags" and rest:
			registry, rest = f"tags/{rest[0]}", rest[1:]
		if not rest or not rel.endswith((".mcfunction", ".json")):
			continue
		text = path.read_text(encoding="utf-8")
		key = (registry, f"{ns}:{'/'.join(rest).rsplit('.', 1)[0]}")
		resources[key] = Resource(registry, "\n".join(commands(text)) if registry == "function" else text)
	return resources


def link(resources: dict[Key, Resource]) -> None:
	""" Fill each resource's references: id tokens in its text, macro patterns, tag values. """
	by_id: dict[str, list[Key]] = {}
	for key in resources:
		by_id.setdefault(key[1], []).append(key)
	for key, res in resources.items():
		for m in ID_TOKEN.finditer(res.text):
			res.refs |= {t for t in token_targets(m, res.text, by_id) if t[0].startswith("tags/") == bool(m.group(1))}
		if key[0].startswith("tags/"):
			res.refs |= tag_values(key[0], json.loads(res.text))
		res.refs.discard(key)


def token_targets(m: re.Match[str], text: str, by_id: dict[str, list[Key]]) -> list[Key]:
	""" Resources an id token can name; a macro token matches every id of its shape. """
	path = m.group(3)
	token = f"{m.group(2)}:{path}"
	if "$(" not in token:
		return by_id.get(token, [])
	# "mgs:$(fire)" is a sound or a model: only a literal folder or a function keyword pins the registry
	is_call = re.search(r"function\s+#?$", text[max(0, m.start() - 12): m.start()]) is not None
	if "/" not in path.split("$(")[0] and not is_call:
		return []
	pattern = re.compile("^" + re.sub(r"\\\$\\\([a-z_0-9]+\\\)", r"[a-z0-9_./\\-]*", re.escape(token)) + "$")
	return [k for rid, keys in by_id.items() if pattern.match(rid) for k in keys]


def entry_id(value: str | JsonDict) -> str:
	""" Id of a tag entry, written either as a string or as {"id": ..., "required": false}. """
	return value if isinstance(value, str) else str(value["id"])


def tag_values(registry: str, tag: JsonDict) -> set[Key]:
	values = [entry_id(v) for v in tag.get("values", [])]
	return {(registry, v[1:]) if v.startswith("#") else (registry.removeprefix("tags/"), v) for v in values}


def missing_calls(resources: dict[Key, Resource]) -> list[str]:
	""" Static calls to a function or function tag of this pack's namespaces that does not exist. """
	own = {key[1].split(":")[0] for key in resources}
	calls = {
		(key[1], ("tags/function" if m.group(1) else "function", m.group(2)))
		for key, res in resources.items() if key[0] == "function" for m in CALL.finditer(res.text)
	}
	return sorted(f"{caller}: calls missing {t[1]}" for caller, t in calls if t[1].split(":")[0] in own and t not in resources)


def reachable(resources: dict[Key, Resource]) -> set[Key]:
	""" Resources reachable from the game's entry points and the pack's public API. """
	stack = [k for k in resources if k[0] == "advancement" or k[1].startswith(("minecraft:", "common_signals:", "mgs:i/"))]
	stack += [k for k in resources if k[0] == "function" and k[1].startswith("mgs:") and not k[1].startswith("mgs:v")]
	seen: set[Key] = set()
	while stack:
		key = stack.pop()
		if key not in seen:
			seen.add(key)
			stack += [r for r in resources[key].refs if r in resources]
	return seen


def server(java: str) -> int:
	""" Start a fresh world with the pack and its libraries, /reload once, stop, report datapack errors. """
	run = WORK / "server"
	if not (run / "server.jar").exists():
		sys.exit(f"put the {MINECRAFT} server.jar in {run} (piston-data.mojang.com)")
	shutil.rmtree(run / "world", ignore_errors=True)
	shutil.copytree(BUILD / "datapack", run / "world/datapacks/mgs", ignore_dangling_symlinks=True)
	libraries_pack(run / "world/datapacks/libs")
	(run / "eula.txt").write_text("eula=true\n")
	(run / "server.properties").write_text(
		"online-mode=false\nlevel-type=minecraft\\:flat\ngenerate-structures=false\ninitial-enabled-packs=vanilla,file/libs,file/mgs\n"
	)
	log, sent = run_server(java, run)
	errors = [line for line in log if SERVER_ERROR.search(line) and "Services Discovery" not in line]
	print(f"{len(errors)} datapack errors or warnings in the server log", *errors, sep="\n")
	return 1 if errors or sent != ["reload", "stop"] else 0


def run_server(java: str, run: Path) -> tuple[list[str], list[str]]:
	""" The server's console lines, and the commands sent: /reload once started, /stop once reloading. """
	process = subprocess.Popen(
		[java, "-jar", "server.jar", "nogui"], cwd=run, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
	)
	assert process.stdin and process.stdout
	log: list[str] = []
	sent: list[str] = []
	for line in process.stdout:
		log.append(line.rstrip())
		command = "reload" if "Done (" in line else "stop" if "Reloading!" in line else ""
		if command:
			sent.append(command)
			process.stdin.write(f"{command}\n")
			process.stdin.flush()
	process.wait()
	return log, sent


def libraries_pack(target: Path) -> None:
	""" The libraries of the committed merged zip, without this project's files and tag entries. """
	merged = zipfile.ZipFile(BUILD / "MCGunsSystem_datapack_with_libs.zip")
	own = {rel for rel, _ in files(BUILD / "datapack") if rel.startswith("data/") and "/tags/" not in rel}
	for name in merged.namelist():
		if name.endswith("/") or name.startswith("data/mgs/") or name in own:
			continue
		data = merged.read(name)
		if "/tags/" in name:
			tag: JsonDict = json.loads(data)
			tag["values"] = [v for v in tag["values"] if not entry_id(v).lstrip("#").startswith("mgs:")]
			data = json.dumps(tag).encode()
		(target / name).parent.mkdir(parents=True, exist_ok=True)
		(target / name).write_bytes(data)


def lint() -> int:
	""" ruff, pyright strict (with the project interpreter) and complexipy over src and scripts. """
	venv = ROOT / ".venv/bin"
	return max(
		subprocess.run([str(venv / "ruff"), "check", "src", "scripts"], cwd=ROOT).returncode,
		subprocess.run([str(venv / "pyright"), "src", "scripts", "--pythonpath", str(venv / "python")], cwd=ROOT).returncode,
		subprocess.run(["uvx", "complexipy", "src", "scripts", "--failed", "--max-complexity-allowed", "15"], cwd=ROOT).returncode,
	)


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("command", choices=("baseline", "check", "validate", "server", "lint"))
	parser.add_argument("--diff", action="store_true", help="check: print the commands each changed function lost and gained")
	parser.add_argument("--no-build", action="store_true", help="use build/ as it is")
	parser.add_argument("--java", default="java", help="server: Java 25 or newer for 26.3, as an absolute path")
	args = parser.parse_args()
	command: str = args.command
	if command != "lint" and not args.no_build:
		build()
	if command == "baseline":
		shutil.rmtree(BASELINE, ignore_errors=True)
		for tree in TREES:
			shutil.copytree(BUILD / tree, BASELINE / tree)
		return 0
	if command == "check":
		return check(show=args.diff)
	if command == "validate":
		return validate()
	if command == "server":
		return server(args.java)
	return lint()


if __name__ == "__main__":
	raise SystemExit(main())

