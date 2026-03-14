
#> mgs:v5.0.0/zombies/mystery_box/show_result
#
# @within	mgs:v5.0.0/zombies/mystery_box/tick
#

# Set display to final result
execute if data storage mgs:zombies mystery_box.result.weapon_id run function mgs:v5.0.0/zombies/mystery_box/show_result_weapon with storage mgs:zombies mystery_box.result
execute unless data storage mgs:zombies mystery_box.result.weapon_id run data modify entity @n[tag=mgs.mb_display] item set from storage mgs:zombies mystery_box.result.display_item

# Start at y=1.5, then descend to y=0.0 over 7.5s (150 ticks)
data merge entity @n[tag=mgs.mb_display] {transformation:{translation:[0f,1.5f,0f]}}
data merge entity @n[tag=mgs.mb_display] {interpolation_duration:150,transformation:{translation:[0f,0f,0f]},start_interpolation:0}

# Tag the box as ready for pickup
data modify storage mgs:zombies mystery_box.ready set value true

# Announce result
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.mystery_box_result_ready","color":"light_purple"},{"translate":"mgs.right_click_to_collect","color":"green","bold":true}]
function mgs:v5.0.0/zombies/feedback/sound_box_ready

