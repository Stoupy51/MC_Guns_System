
#> mgs:v5.0.0/zombies/mystery_box/collect
#
# @within	mgs:v5.0.0/zombies/mystery_box/on_right_click
#

# Give the result item to the player via its give function
execute if data storage mgs:zombies mystery_box.result.give_function run function mgs:v5.0.0/zombies/mystery_box/give_via_function

# If the give flow failed (e.g. invalid selected slot), keep result ready for retry.
execute if score #wb_purchase_mode mgs.data matches -1 run return 0

# Announce
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_collected","color":"green"},{"storage":"mgs:zombies","nbt":"mystery_box.result.weapon_id","color":"gold"},[{"text":" ","color":"green"}, {"translate":"mgs.from_the_mystery_box"}]]
function mgs:v5.0.0/zombies/feedback/sound_success

# Reset box
function mgs:v5.0.0/zombies/mystery_box/reset

