
#> mgs:v5.4.1/maps/editor/dedupe/mystery_box_pos
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/maps/editor/remove_duplicates [ at @s ]
#

execute if entity @s[tag=mgs.ed_dup] run return 0
tag @s add mgs.ed_keep
execute unless entity @e[type=minecraft:marker,tag=mgs.element.mystery_box_pos,tag=!mgs.ed_keep,distance=..0.01] run return 0
function mgs:v5.4.1/maps/editor/dedupe_read
execute as @e[type=minecraft:marker,tag=mgs.element.mystery_box_pos,tag=!mgs.ed_keep,distance=..0.01] run function mgs:v5.4.1/maps/editor/dedupe_same

