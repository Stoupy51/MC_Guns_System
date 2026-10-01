""" Collecting a result, naming the weapon that was given and resetting the box. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.feedback import ZombiesFeedback
from ....helpers import MGS_TAG
from ....progression import Xp
from .shared import owned_gun_macro_cd


# Functions
def write_mystery_box_collect() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	owned_gun_cd: str = owned_gun_macro_cd(ns)

	## Run from box_click as the player, at the box.
	write_versioned_function("zombies/mystery_box/collect", f"""
data modify storage {ns}:zombies mystery_box.result set from entity @n[tag={ns}.mb_display,distance=..3] item.components."minecraft:custom_data".{ns}.mb_result

scoreboard players set #wb_purchase_done {ns}.data 0
scoreboard players set #wb_purchase_mode {ns}.data -1
execute if data storage {ns}:zombies mystery_box.result.give_function run function {ns}:v{version}/zombies/mystery_box/give_via_function

# A failed give (invalid selected slot) keeps the result for a retry.
execute if score #wb_purchase_done {ns}.data matches 0 run return 0

execute if data storage {ns}:zombies mystery_box.result.weapon_id run function {ns}:v{version}/zombies/mystery_box/capture_collected_name with storage {ns}:zombies mystery_box.result

tellraw @s [{MGS_TAG},{{"text":"You collected ","color":"green"}},{{"storage":"{ns}:temp","nbt":"_mb_collected_name","interpret":true}},{{"text":" from the Mystery Box.","color":"green"}},{Xp.suffix("zb", "mystery_box")}]
{Xp.give("zb", "mystery_box")}
{ZombiesFeedback.zb_sound('success')}
{ZombiesFeedback.zb_sound('box_close')}

# The buyer lives on the display, so nothing to clear on the player.
function {ns}:v{version}/zombies/mystery_box/close_lid
kill @n[tag={ns}.mb_display,distance=..3]

# A Fire Sale that ended during pulls cleans up once none remain.
execute if score #mb_fs_cleanup_pending {ns}.data matches 1 unless entity @e[tag={ns}.mb_display] run function {ns}:v{version}/zombies/mystery_box/fire_sale_cleanup

# A Fire Sale box is hidden again once its pull is done.
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

	## Run as the display, at the box.
	write_versioned_function("zombies/mystery_box/reset_one", f"""
function {ns}:v{version}/zombies/mystery_box/close_lid

kill @s

# A Fire Sale that ended during pulls cleans up once none remain.
execute if score #mb_fs_cleanup_pending {ns}.data matches 1 unless entity @e[tag={ns}.mb_display] run function {ns}:v{version}/zombies/mystery_box/fire_sale_cleanup

# A Fire Sale box is hidden again once its pull is done.
function {ns}:v{version}/zombies/mystery_box/sync_interaction_visibility
""")

