""" Collecting a result, naming the weapon that was given and resetting the box. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.feedback import ZombiesFeedback
from ....helpers import MGS_TAG
from .shared import owned_gun_macro_cd


# Functions
def write_mystery_box_collect() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	owned_gun_cd: str = owned_gun_macro_cd(ns)

	## Collect this box's result (called from box_click, @s = player, positioned at the box)
	write_versioned_function("zombies/mystery_box/collect", f"""
# Load the result baked onto this box's display
data modify storage {ns}:zombies mystery_box.result set from entity @n[tag={ns}.mb_display,distance=..3] item.components."minecraft:custom_data".{ns}.mb_result

# Give the result item to the player via its give function
scoreboard players set #wb_purchase_done {ns}.data 0
scoreboard players set #wb_purchase_mode {ns}.data -1
execute if data storage {ns}:zombies mystery_box.result.give_function run function {ns}:v{version}/zombies/mystery_box/give_via_function

# If the give flow failed (e.g. invalid selected slot), keep the result ready for retry.
execute if score #wb_purchase_done {ns}.data matches 0 run return 0

# Resolve the collected weapon display name from the given item.
execute if data storage {ns}:zombies mystery_box.result.weapon_id run function {ns}:v{version}/zombies/mystery_box/capture_collected_name with storage {ns}:zombies mystery_box.result

# Announce + sounds
tellraw @s [{MGS_TAG},{{"text":"You collected ","color":"green"}},{{"storage":"{ns}:temp","nbt":"_mb_collected_name","interpret":true}},{{"text":" from the Mystery Box.","color":"green"}}]
{ZombiesFeedback.zb_sound('success')}
{ZombiesFeedback.zb_sound('box_close')}

# Close this box's lid and remove its display (buyer is tracked per-display, nothing to clear)
function {ns}:v{version}/zombies/mystery_box/close_lid
kill @n[tag={ns}.mb_display,distance=..3]

# If a Fire Sale ended while pulls were in progress, finish temp-box cleanup once none remain
execute if score #mb_fs_cleanup_pending {ns}.data matches 1 unless entity @e[tag={ns}.mb_display] run function {ns}:v{version}/zombies/mystery_box/fire_sale_cleanup

# This box's pull is done: if it's no longer usable (e.g. a Fire-Sale box after the sale), hide it
function {ns}:v{version}/zombies/mystery_box/sync_interaction_visibility
""")

	write_versioned_function("zombies/mystery_box/capture_collected_name", f"""
$data modify storage {ns}:temp _mb_collected_name set value [{{"text":"$(weapon_id)","color":"gold"}}]
scoreboard players set #mb_name_found {ns}.data 0

$execute if score #mb_name_found {ns}.data matches 0 if items entity @s hotbar.1 *[custom_data~{owned_gun_cd}] run function {ns}:v{version}/zombies/mystery_box/capture_collected_name_slot {{slot:"hotbar.1"}}
$execute if score #mb_name_found {ns}.data matches 0 if items entity @s hotbar.2 *[custom_data~{owned_gun_cd}] run function {ns}:v{version}/zombies/mystery_box/capture_collected_name_slot {{slot:"hotbar.2"}}
$execute if score #mb_name_found {ns}.data matches 0 if items entity @s hotbar.3 *[custom_data~{owned_gun_cd}] run function {ns}:v{version}/zombies/mystery_box/capture_collected_name_slot {{slot:"hotbar.3"}}
$execute if score #mb_name_found {ns}.data matches 0 if items entity @s hotbar.6 *[custom_data~{owned_gun_cd}] run function {ns}:v{version}/zombies/mystery_box/capture_collected_name_slot {{slot:"hotbar.6"}}
""")

	write_versioned_function("zombies/mystery_box/capture_collected_name_slot", f"""
tag @s add {ns}.mb_name_reader
$execute summon item_display run function {ns}:v{version}/zombies/mystery_box/extract_collected_item_name {{slot:"$(slot)"}}
tag @s remove {ns}.mb_name_reader
scoreboard players set #mb_name_found {ns}.data 1
""")

	write_versioned_function("zombies/mystery_box/extract_collected_item_name", f"""
$item replace entity @s contents from entity @p[tag={ns}.mb_name_reader] $(slot)
data modify storage {ns}:temp _mb_collected_name set from entity @s item.components."minecraft:item_name"
kill @s
""")

	write_versioned_function("zombies/mystery_box/give_via_function", f"""
function {ns}:v{version}/zombies/mystery_box/run_give with storage {ns}:zombies mystery_box.result
""")

	write_versioned_function("zombies/mystery_box/run_give", """
$function $(give_function)
""")

	## Reset a single pull (@s = display, positioned at the box). Expires the display & closes its lid.
	write_versioned_function("zombies/mystery_box/reset_one", f"""
# Close this box's lid
function {ns}:v{version}/zombies/mystery_box/close_lid

# Remove the display (buyer is tracked per-display, nothing to clear on the player)
kill @s

# If a Fire Sale ended while pulls were in progress, finish temp-box cleanup once none remain
execute if score #mb_fs_cleanup_pending {ns}.data matches 1 unless entity @e[tag={ns}.mb_display] run function {ns}:v{version}/zombies/mystery_box/fire_sale_cleanup

# This box's pull ended: if it's no longer usable (e.g. a Fire-Sale box after the sale), hide it
function {ns}:v{version}/zombies/mystery_box/sync_interaction_visibility
""")

