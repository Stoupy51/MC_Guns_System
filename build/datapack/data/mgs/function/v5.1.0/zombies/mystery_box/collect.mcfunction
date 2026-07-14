
#> mgs:v5.1.0/zombies/mystery_box/collect
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/mystery_box/box_click
#

# Load the result baked onto this box's display
data modify storage mgs:zombies mystery_box.result set from entity @n[tag=mgs.mb_display,distance=..3] item.components."minecraft:custom_data".mgs.mb_result

# Give the result item to the player via its give function
scoreboard players set #wb_purchase_done mgs.data 0
scoreboard players set #wb_purchase_mode mgs.data -1
execute if data storage mgs:zombies mystery_box.result.give_function run function mgs:v5.1.0/zombies/mystery_box/give_via_function

# If the give flow failed (e.g. invalid selected slot), keep the result ready for retry.
execute if score #wb_purchase_done mgs.data matches 0 run return 0

# Resolve the collected weapon display name from the given item.
execute if data storage mgs:zombies mystery_box.result.weapon_id run function mgs:v5.1.0/zombies/mystery_box/capture_collected_name with storage mgs:zombies mystery_box.result

# Announce + sounds
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_collected","color":"green"},{"storage":"mgs:temp","nbt":"_mb_collected_name","interpret":true},[{"text":" ","color":"green"}, {"translate":"mgs.from_the_mystery_box"}]]
function mgs:v5.1.0/zombies/feedback/sound_success
function mgs:v5.1.0/zombies/feedback/sound_box_close

# Clear this player's pull state, close this box's lid, and remove its display
scoreboard players set @s mgs.mb.buying 0
function mgs:v5.1.0/zombies/mystery_box/close_lid
kill @n[tag=mgs.mb_display,distance=..3]

# If a Fire Sale ended while pulls were in progress, finish temp-box cleanup once none remain
execute if score #mb_fs_cleanup_pending mgs.data matches 1 unless entity @e[tag=mgs.mb_display] run function mgs:v5.1.0/zombies/mystery_box/fire_sale_cleanup

