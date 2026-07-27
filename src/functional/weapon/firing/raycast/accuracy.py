""" Resolving a weapon's spread from player state and applying it as a random rotation. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.keys import ACCURACY_BASE, ACCURACY_JUMP, ACCURACY_SNEAK, ACCURACY_SPRINT, ACCURACY_WALK


# Functions
def write_accuracy() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Accuracy Get values
	write_versioned_function("raycast/accuracy/get_value", f"""
## Order is important: Sneak+Air=Walk > Jump > Sneak > Sprint > Walk > Base
data remove storage {ns}:gun accuracy

# If sneaking in the air, treat as walking (not jump accuracy)
execute unless predicate {ns}:v{version}/is_on_ground if predicate {ns}:v{version}/is_sneaking run return run data modify storage {ns}:gun accuracy set from storage {ns}:gun all.stats.{ACCURACY_WALK}

# If not on ground (and not sneaking), return jump accuracy
execute unless predicate {ns}:v{version}/is_on_ground run return run data modify storage {ns}:gun accuracy set from storage {ns}:gun all.stats.{ACCURACY_JUMP}

# If sneaking, return sneak accuracy
execute if predicate {ns}:v{version}/is_sneaking run return run data modify storage {ns}:gun accuracy set from storage {ns}:gun all.stats.{ACCURACY_SNEAK}

# If sprinting, return sprint accuracy
execute if predicate {ns}:v{version}/is_sprinting run return run data modify storage {ns}:gun accuracy set from storage {ns}:gun all.stats.{ACCURACY_SPRINT}

# If moving horizontally, return walk accuracy
execute if predicate {ns}:v{version}/is_moving run return run data modify storage {ns}:gun accuracy set from storage {ns}:gun all.stats.{ACCURACY_WALK}

# Else, return base accuracy
data modify storage {ns}:gun accuracy set from storage {ns}:gun all.stats.{ACCURACY_BASE}
""")

	# Deadshot Daiquiri: scale the resolved spread value to 65% (read back by apply_spread per pellet)
	write_versioned_function("raycast/accuracy/deadshot_scale", f"""
execute store result score #ds_acc {ns}.data run data get storage {ns}:gun accuracy 1000
scoreboard players set #ds_num {ns}.data 65
scoreboard players set #ds_den {ns}.data 100
scoreboard players operation #ds_acc {ns}.data *= #ds_num {ns}.data
scoreboard players operation #ds_acc {ns}.data /= #ds_den {ns}.data
execute store result storage {ns}:gun accuracy double 0.001 run scoreboard players get #ds_acc {ns}.data
""")

	# Apply random rotation spread
	write_versioned_function("raycast/accuracy/apply_spread", f"""
# Get random uniform rotation spread (https://docs.mcbookshelf.dev/en/latest/modules/random.html#random-distributions)
data modify storage {ns}:input with set value {{}}
execute store result storage {ns}:input with.min int -1 run data get storage {ns}:gun accuracy
execute store result storage {ns}:input with.max int 1 run data get storage {ns}:gun accuracy
function #bs.random:uniform with storage {ns}:input with

# Add horizontal rotation (divided by 100) (https://docs.mcbookshelf.dev/en/latest/modules/position.html#add-position-and-rotation)
scoreboard players operation @s bs.rot.h = $random.uniform bs.out
function #bs.position:add_rot_h {{scale: 0.01}}

# Get a new random rotation spread
function #bs.random:uniform with storage {ns}:input with

# Add vertical rotation (divided by 100)
scoreboard players operation @s bs.rot.v = $random.uniform bs.out
function #bs.position:add_rot_v {{scale: 0.01}}
""")

