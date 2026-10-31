""" The Fire Sale: every spot becomes a real box, then the temp ones are torn down. """
# Imports
from stewbeet import Mem, write_versioned_function

from .shared import INTERACTION_LIFT


# Functions
def write_fire_sale() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Remember the original box, make every position usable, spawn temporary boxes.
	write_versioned_function("zombies/mystery_box/fire_sale_start", f"""
tag @e[tag={ns}.mystery_box_active] add {ns}.mb_orig_active
tag @e[tag={ns}.mystery_box_pos] add {ns}.mb_fs_active

# The inactive spots become real boxes, so their grayed crates go.
kill @e[tag={ns}.mb_disabled]

# Before summoning the boxes: a hidden interaction entity sits 512 blocks under its spot, and the chests are summoned `at @s`.
function {ns}:v{version}/zombies/mystery_box/sync_interaction_visibility

execute as @e[tag={ns}.mystery_box_pos,tag=!{ns}.mystery_box_active] at @s positioned ~ ~-{INTERACTION_LIFT} ~ run function {ns}:v{version}/zombies/mystery_box/summon_presence {{extra_tags:',"{ns}.mb_temp"'}}
""")

	# Clean up now if idle, else when the last pull resets, so a box in use is not removed mid-spin.
	write_versioned_function("zombies/mystery_box/fire_sale_end", f"""
tag @e[tag={ns}.mb_fs_active] remove {ns}.mb_fs_active
# Boxes with a pull in progress stay reachable, so buyers can still collect.
function {ns}:v{version}/zombies/mystery_box/sync_interaction_visibility
execute if entity @e[tag={ns}.mb_display] run return run scoreboard players set #mb_fs_cleanup_pending {ns}.data 1
function {ns}:v{version}/zombies/mystery_box/fire_sale_cleanup
""")

	write_versioned_function("zombies/mystery_box/fire_sale_cleanup", f"""
# The active box never changes during a Fire Sale, so its tag is left alone.
tag @e[tag={ns}.mb_orig_active] remove {ns}.mb_orig_active
kill @e[tag={ns}.mb_temp]
scoreboard players set #mb_fs_cleanup_pending {ns}.data 0

function {ns}:v{version}/zombies/mystery_box/sync_interaction_visibility

function {ns}:v{version}/zombies/mystery_box/refresh_disabled
""")

