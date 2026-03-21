
#> mgs:v5.0.0/zombies/mystery_box/collect
#
# @within	mgs:v5.0.0/zombies/mystery_box/on_right_click
#

# Give the result item to the player via its give function
scoreboard players set #wb_purchase_done mgs.data 0
scoreboard players set #wb_purchase_mode mgs.data -1
execute if data storage mgs:zombies mystery_box.result.give_function run function mgs:v5.0.0/zombies/mystery_box/give_via_function

# If the give flow failed (e.g. invalid selected slot), keep result ready for retry.
execute if score #wb_purchase_done mgs.data matches 0 run return 0

# Resolve the collected weapon display name from the given item.
execute if data storage mgs:zombies mystery_box.result.weapon_id run function mgs:v5.0.0/zombies/mystery_box/capture_collected_name with storage mgs:zombies mystery_box.result

# Announce
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_collected","color":"green"},{"storage":"mgs:temp","nbt":"_mb_collected_name","interpret":true},[{"text":" ","color":"green"}, {"translate":"mgs.from_the_mystery_box"}]]
function mgs:v5.0.0/zombies/feedback/sound_success

# Track pulls and sometimes move the box.
function mgs:v5.0.0/zombies/mystery_box/maybe_move_after_pull

# Reset box
function mgs:v5.0.0/zombies/mystery_box/reset

