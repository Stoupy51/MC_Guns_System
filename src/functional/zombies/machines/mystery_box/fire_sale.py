""" The Fire Sale: every spot becomes a real box, then the temp ones are torn down. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from .shared import MB_CLOSED_TF


# Functions
def write_fire_sale() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Begin a Fire Sale: remember the original box, flag all positions usable, spawn temp boxes.
	write_versioned_function("zombies/mystery_box/fire_sale_start", f"""
tag @e[tag={ns}.mystery_box_active] add {ns}.mb_orig_active
tag @e[tag={ns}.mystery_box_pos] add {ns}.mb_fs_active

# Inactive spots become real temp boxes during the sale — clear their grayed disabled crates first.
kill @e[tag={ns}.mb_disabled]

# Every box is usable now: bring all interaction entities back into reach. This MUST happen before
# the temp boxes are summoned below — a hidden interaction entity is parked 512 blocks under its
# real position (see interaction_hide), and the chest models are summoned `at @s`, so summoning
# first buried every fire-sale chest underground: the box was usable but its model was invisible.
function {ns}:v{version}/zombies/mystery_box/sync_interaction_visibility

execute as @e[tag={ns}.mystery_box_pos,tag=!{ns}.mystery_box_active] at @s run function {ns}:v{version}/zombies/mystery_box/fire_sale_summon_box
""")

	write_versioned_function("zombies/mystery_box/fire_sale_summon_box", f"""
data modify storage {ns}:temp _mb_fs.yaw set value 0.0f
data modify storage {ns}:temp _mb_fs.yaw set from entity @s Rotation[0]
function {ns}:v{version}/zombies/mystery_box/summon_temp_box with storage {ns}:temp _mb_fs
""")

	write_versioned_function("zombies/mystery_box/summon_temp_box", f"""
$execute positioned ~ ~-0.9 ~ run summon minecraft:item_display ~ ~ ~ {{Rotation:[$(yaw),0f],Tags:["{ns}.mb_presence","{ns}.mb_base","{ns}.mb_temp","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:chest",count:1,components:{{"minecraft:item_model":"{ns}:mystery_box_base"}}}},transformation:{MB_CLOSED_TF}}}
$execute positioned ~ ~-0.9 ~ run summon minecraft:item_display ~ ~ ~ {{Rotation:[$(yaw),0f],Tags:["{ns}.mb_presence","{ns}.mb_lid","{ns}.mb_temp","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:chest",count:1,components:{{"minecraft:item_model":"{ns}:mystery_box_lid"}}}},transformation:{MB_CLOSED_TF}}}
""")

	# End a Fire Sale: stop allowing temp pulls; clean up now if idle, else defer until the in-progress pull resets (so a box being used isn't yanked mid-spin).
	write_versioned_function("zombies/mystery_box/fire_sale_end", f"""
tag @e[tag={ns}.mb_fs_active] remove {ns}.mb_fs_active
# Re-hide interaction entities of boxes that are no longer usable (boxes with a pull still in
# progress stay reachable via the sync's pull-in-progress check, so buyers can still collect).
function {ns}:v{version}/zombies/mystery_box/sync_interaction_visibility
# If any pull is in progress, defer cleanup until the last display resets; otherwise clean up now.
execute if entity @e[tag={ns}.mb_display] run return run scoreboard players set #mb_fs_cleanup_pending {ns}.data 1
function {ns}:v{version}/zombies/mystery_box/fire_sale_cleanup
""")

	write_versioned_function("zombies/mystery_box/fire_sale_cleanup", f"""
# Remove every temporary box and clear Fire-Sale bookkeeping. The active box never changes during
# a Fire Sale, so we must NOT touch the mystery_box_active tag here (doing so could strip it off
# every box if state is inconsistent, leaving no usable box).
tag @e[tag={ns}.mb_orig_active] remove {ns}.mb_orig_active
kill @e[tag={ns}.mb_temp]
scoreboard players set #mb_fs_cleanup_pending {ns}.data 0

# Non-active boxes are dead again: tuck their interaction entities away
function {ns}:v{version}/zombies/mystery_box/sync_interaction_visibility

# The temp boxes are gone: restore the grayed disabled crates at the inactive spots
function {ns}:v{version}/zombies/mystery_box/refresh_disabled
""")

