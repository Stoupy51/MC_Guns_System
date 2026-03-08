
#> mgs:v5.0.0/zombies/mystery_box/collect
#
# @executed	at @e[tag=mgs.mystery_box_active,limit=1] & as @p[distance=..3,scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.0.0/zombies/mystery_box/check_collect [ at @e[tag=mgs.mystery_box_active,limit=1] & as @p[distance=..3,scores={mgs.zb.in_game=1}] ]
#

# Give the result item to the player via its give function
execute if data storage mgs:zombies mystery_box.result.give_function run function mgs:v5.0.0/zombies/mystery_box/give_via_function

# Announce
tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.you_collected_a_weapon_from_the_mystery_box","color":"green"}]

# Reset box
function mgs:v5.0.0/zombies/mystery_box/reset

