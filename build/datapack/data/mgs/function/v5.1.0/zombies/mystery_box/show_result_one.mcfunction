
#> mgs:v5.1.0/zombies/mystery_box/show_result_one
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.1.0/zombies/mystery_box/spin_tick_one
#

# Box will move (active box only): teddy bear path
execute if score @s mgs.mb.willmove matches 1 run return run function mgs:v5.1.0/zombies/mystery_box/show_bear_result

# Remember this box's id, then pick + reroll the result as its buyer
scoreboard players operation #this_box mgs.data = @s mgs.mb.box
data remove storage mgs:zombies mystery_box.result
scoreboard players set #mb_owned mgs.data 0
execute as @a[scores={mgs.zb.in_game=1}] if score @s mgs.mb.buying = #this_box mgs.data run function mgs:v5.1.0/zombies/mystery_box/pick_for_buyer

# All owned / empty pool: refund the buyer and cancel this pull
execute if score #mb_owned mgs.data matches 1 run function mgs:v5.1.0/zombies/mystery_box/result_all_owned
execute if score #mb_owned mgs.data matches 1 run return run function mgs:v5.1.0/zombies/mystery_box/reset_one

# Set this display to the final weapon and bake the result onto it for collect
execute if data storage mgs:zombies mystery_box.result.weapon_id run function mgs:v5.1.0/zombies/mystery_box/show_result_weapon_one with storage mgs:zombies mystery_box.result
execute unless data storage mgs:zombies mystery_box.result.weapon_id run data modify entity @s item set from storage mgs:zombies mystery_box.result.display_item
data modify entity @s item.components."minecraft:custom_data".mgs.mb_result set from storage mgs:zombies mystery_box.result

# Descend into place over 7.5s (150 ticks)
data merge entity @s {transformation:{translation:[0f,1.5f,0f]}}
data merge entity @s {interpolation_duration:150,transformation:{translation:[0f,0f,0f]},start_interpolation:0}

# Tell only the buyer it is ready
execute as @a[scores={mgs.zb.in_game=1}] if score @s mgs.mb.buying = #this_box mgs.data run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.mystery_box_result_ready","color":"light_purple"},{"translate":"mgs.right_click_to_collect","color":"green","bold":true}]

