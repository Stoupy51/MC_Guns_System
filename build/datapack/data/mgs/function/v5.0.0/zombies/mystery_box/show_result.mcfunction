
#> mgs:v5.0.0/zombies/mystery_box/show_result
#
# @within	mgs:v5.0.0/zombies/mystery_box/tick
#

# Set display to final result
data modify entity @n[tag=mgs.mb_display] item set from storage mgs:zombies mystery_box.result.display_item

# Smooth settle to final position with interpolation
data merge entity @n[tag=mgs.mb_display] {transformation:{translation:[0f,1.0f,0f],scale:[0.8f,0.8f,0.8f]},start_interpolation:0}

# Tag the box as ready for pickup
data modify storage mgs:zombies mystery_box.ready set value true

# Announce result
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.mystery_box_result_ready","color":"light_purple"},{"translate": "mgs.right_click_to_collect","color":"green","bold":true}]

