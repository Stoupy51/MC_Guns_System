
#> mgs:v5.0.0/zombies/mystery_box/show_result
#
# @within	mgs:v5.0.0/zombies/mystery_box/tick
#

# Set display to final result
execute as @e[tag=mgs.mb_display,limit=1] run data modify entity @s item set from storage mgs:zombies mystery_box.result.display_item

# Announce result to buyer
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.mystery_box_result_ready","color":"light_purple"},{"translate": "mgs.right_click_to_collect","color":"green","bold":true}]

# Tag the box as ready for pickup
data modify storage mgs:zombies mystery_box.ready set value true

