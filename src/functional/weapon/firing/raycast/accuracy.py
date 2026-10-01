""" Resolving a weapon's spread from player state and applying it as a random rotation. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.keys import (
	ACCURACY_BASE,
	ACCURACY_JUMP,
	ACCURACY_SNEAK,
	ACCURACY_SPRINT,
	ACCURACY_WALK,
)


# Functions
def write_accuracy() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("raycast/accuracy/get_value", f"""
## Order matters: sneak in the air counts as walk, then jump, sneak, sprint, walk, base.
data remove storage {ns}:gun accuracy

execute unless predicate {ns}:v{version}/is_on_ground if predicate {ns}:v{version}/is_sneaking run return run data modify storage {ns}:gun accuracy set from storage {ns}:gun all.stats.{ACCURACY_WALK}

execute unless predicate {ns}:v{version}/is_on_ground run return run data modify storage {ns}:gun accuracy set from storage {ns}:gun all.stats.{ACCURACY_JUMP}

execute if predicate {ns}:v{version}/is_sneaking run return run data modify storage {ns}:gun accuracy set from storage {ns}:gun all.stats.{ACCURACY_SNEAK}

execute if predicate {ns}:v{version}/is_sprinting run return run data modify storage {ns}:gun accuracy set from storage {ns}:gun all.stats.{ACCURACY_SPRINT}

execute if predicate {ns}:v{version}/is_moving run return run data modify storage {ns}:gun accuracy set from storage {ns}:gun all.stats.{ACCURACY_WALK}

data modify storage {ns}:gun accuracy set from storage {ns}:gun all.stats.{ACCURACY_BASE}
""")

	# Deadshot Daiquiri: spread to 65% (apply_spread reads it per pellet).
	write_versioned_function("raycast/accuracy/deadshot_scale", f"""
execute store result score #ds_acc {ns}.data run data get storage {ns}:gun accuracy 1000
scoreboard players set #ds_num {ns}.data 65
scoreboard players set #ds_den {ns}.data 100
scoreboard players operation #ds_acc {ns}.data *= #ds_num {ns}.data
scoreboard players operation #ds_acc {ns}.data /= #ds_den {ns}.data
execute store result storage {ns}:gun accuracy double 0.001 run scoreboard players get #ds_acc {ns}.data
""")

	write_versioned_function("raycast/accuracy/apply_spread", f"""
# https://docs.mcbookshelf.dev/en/latest/modules/random.html#random-distributions
data modify storage {ns}:input with set value {{}}
execute store result storage {ns}:input with.min int -1 run data get storage {ns}:gun accuracy
execute store result storage {ns}:input with.max int 1 run data get storage {ns}:gun accuracy
function #bs.random:uniform with storage {ns}:input with

# Divided by 100 (https://docs.mcbookshelf.dev/en/latest/modules/position.html#add-position-and-rotation).
scoreboard players operation @s bs.rot.h = $random.uniform bs.out
function #bs.position:add_rot_h {{scale: 0.01}}

function #bs.random:uniform with storage {ns}:input with

# Divided by 100.
scoreboard players operation @s bs.rot.v = $random.uniform bs.out
function #bs.position:add_rot_v {{scale: 0.01}}
""")

