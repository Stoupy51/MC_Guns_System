""" What an operator does once: switching the public lobby on or off, and placing the controls display. """
# Imports
from dataclasses import dataclass

from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG
from .queues import queues


# Classes
@dataclass(frozen=True)
class Control:
	keys: tuple[str, ...]
	""" Keybind ids, shown with each player's own binding. """
	action: str


# Constants
CONTROLS: list[Control] = [
	Control(keys=("key.use",), action="Shoot, throw a grenade"),
	Control(keys=("key.sneak",), action="Aim down sights"),
	Control(keys=("key.attack", "key.swapOffhand"), action="Reload"),
	Control(keys=("key.drop",), action="Switch fire mode"),
	Control(keys=("key.sprint",), action="Sprint, it uses stamina"),
	Control(keys=("key.sneak",), action="Plant or defuse at a bomb site"),
	Control(keys=("key.use",), action="Buy at a wall weapon or a machine (Zombies)"),
	Control(keys=("key.sneak",), action="Repair a barricade (Zombies)"),
	Control(keys=("key.quickActions",), action="Menu: play, class, stats"),
]


# Functions
def write_lobby_admin() -> None:
	ns: str = Mem.ctx.project_id

	## The players online now count as seen, or the login check would take them all for returning players.
	write_versioned_function("lobby/public/enable", f"""
execute unless data storage {ns}:config lobby.dimension run return run tellraw @s [{MGS_TAG},{{"text":"Set the lobby first, with Set Lobby Here.","color":"red"}}]
scoreboard players set #public_lobby {ns}.config 1
scoreboard players operation @a {ns}.lobby.seen = #now {ns}.lobby.seen
tellraw @s [{MGS_TAG},{{"text":"Public lobby on: players join a mode from the menu or the chat, vote and play with no operator.","color":"green"}}]
""")

	write_versioned_function("lobby/public/disable", "\n".join((
		f"scoreboard players set #public_lobby {ns}.config 0",
		*(f"scoreboard players set #lv_{queue.prefix}_round {ns}.data 0" for queue in queues()),
		f"scoreboard players reset * {ns}.lobby.queue",
		f"scoreboard players reset * {ns}.lobby.choice",
		f'tellraw @s [{MGS_TAG},{{"text":"Public lobby off: games running go on, queues and votes are cleared.","color":"yellow"}}]',
	)))

	lines: str = "".join(
		',"\\n",' + ',{"text":" or ","color":"gray"},'.join(f'{{"keybind":"{key}","color":"yellow"}}' for key in control.keys)
		+ f',"  ",{{"text":"{control.action}","color":"white"}}'
		for control in CONTROLS
	)
	## Vertical billboard: it turns to face each reader. Placing again replaces it.
	write_versioned_function("lobby/controls/place", f"""
kill @e[type=minecraft:text_display,tag={ns}.lobby_controls]
summon minecraft:text_display ~ ~1.5 ~ {{Tags:["{ns}.lobby_controls"],billboard:"vertical",alignment:"left",line_width:400,text:["",{{"text":"Controls","color":"gold","bold":true}}{lines}]}}
tellraw @s [{MGS_TAG},{{"text":"Controls display placed where you stand.","color":"green"}}]
""")

