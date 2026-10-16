""" Shared teleports: to a position, and back to the lobby when a game ends. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..helpers import MGS_TAG


# Functions
def write_shared_teleport_functions() -> None:
		ns: str = Mem.ctx.project_id
		version: str = Mem.ctx.project_version

		## Teleport to position (macro) Usage: function shared/tp_to_position with storage {ns}:temp _tp
		write_versioned_function("shared/tp_to_position", "$tp @s $(x) $(y) $(z)")

		## Run as a player from the config menu: where they stand becomes the lobby, dimension and rotation included.
		write_versioned_function("lobby/set", f"""
data modify storage {ns}:config lobby set value {{}}
data modify storage {ns}:config lobby.dimension set from entity @s Dimension
data modify storage {ns}:config lobby.x set from entity @s Pos[0]
data modify storage {ns}:config lobby.y set from entity @s Pos[1]
data modify storage {ns}:config lobby.z set from entity @s Pos[2]
data modify storage {ns}:config lobby.yaw set from entity @s Rotation[0]
data modify storage {ns}:config lobby.pitch set from entity @s Rotation[1]
tellraw @s [{MGS_TAG},{{"text":"Lobby set where you stand. Players return here when their game ends.","color":"green"}}]
""")

		write_versioned_function("lobby/clear", f"""
data remove storage {ns}:config lobby
tellraw @s [{MGS_TAG},{{"text":"Lobby cleared. Players stay where their game ends.","color":"yellow"}}]
""")

		## Run as a player whose game just ended. Nothing happens until a lobby is set.
		write_versioned_function("lobby/return", f"""
execute if data storage {ns}:config lobby.dimension run function {ns}:v{version}/lobby/teleport with storage {ns}:config lobby
""")
		write_versioned_function("lobby/teleport", "$execute in $(dimension) run tp @s $(x) $(y) $(z) $(yaw) $(pitch)")

