
#> mgs:v5.0.0/zombies/mystery_box/show_bear_result
#
# @within	mgs:v5.0.0/zombies/mystery_box/show_result
#

# Replace display with teddy bear
loot replace entity @n[tag=mgs.mb_display] contents loot mgs:i/mystery_box_bear

# Rise bear out of the box (like normal result)
data merge entity @n[tag=mgs.mb_display] {transformation:{translation:[0f,1.5f,0f]}}
data merge entity @n[tag=mgs.mb_display] {interpolation_duration:40,transformation:{translation:[0f,0.5f,0f]},start_interpolation:0}

# Refund the buyer
execute as @a[tag=mgs.mb_buyer] run scoreboard players operation @s mgs.zb.points += #zb_mystery_box_price mgs.config
tag @a[tag=mgs.mb_buyer] remove mgs.mb_buyer

# Stop spin, start move animation timer
data modify storage mgs:zombies mystery_box.spinning set value false
scoreboard players set #mb_move_timer mgs.data 280

# Announce
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.the_mystery_box_is_moving_2","color":"yellow","bold":true}]
execute as @n[tag=mgs.mystery_box_active] at @s run function mgs:v5.0.0/zombies/feedback/sound_box_bye_bye

