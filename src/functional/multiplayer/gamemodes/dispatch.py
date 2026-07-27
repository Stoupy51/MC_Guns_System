""" The gamemode list and the dispatch block that routes a lifecycle script to the active one. """
# Constants
GAMEMODES: list[str] = ["ffa", "tdm", "dom", "hp", "snd"]
""" Every multiplayer gamemode, the single source of truth for dispatch blocks. """


# Functions
def gm_dispatch(ns: str, version: str, script: str, ret: bool = False) -> str:
	""" Build the per-gamemode dispatch lines for a given script (setup/cleanup/tick/on_kill).

	Args:
		ns      (str): The project namespace.
		version (str): The project version, used to build the function paths.
		script  (str): Lifecycle script name, e.g. "setup" or "on_kill".
		ret     (bool): Wrap in `return run` so the caller stops at the first matching gamemode.
	Returns:
		str: One `execute if data storage ...` line per gamemode.

	Examples:
		>>> gm_dispatch("mgs", "1.0", "tick").splitlines()[0]
		'execute if data storage mgs:multiplayer game{gamemode:"ffa"} run function mgs:v1.0/multiplayer/gamemodes/ffa/tick'
		>>> gm_dispatch("mgs", "1.0", "on_kill", ret=True).splitlines()[0]
		'execute if data storage mgs:multiplayer game{gamemode:"ffa"} run return run function mgs:v1.0/multiplayer/gamemodes/ffa/on_kill'
	"""
	run: str = "run return run" if ret else "run"
	return "\n".join(
		f'execute if data storage {ns}:multiplayer game{{gamemode:"{gm}"}} {run} function {ns}:v{version}/multiplayer/gamemodes/{gm}/{script}'
		for gm in GAMEMODES
	)

