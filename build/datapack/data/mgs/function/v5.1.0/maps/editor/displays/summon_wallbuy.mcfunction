
#> mgs:v5.1.0/maps/editor/displays/summon_wallbuy
#
# @executed	as @e[tag=mgs.element.wallbuy] & at @s
#
# @within	mgs:v5.1.0/maps/editor/displays/wallbuy with storage mgs:temp _ed_disp
#
# @args		yaw (unknown)
#			weapon_id (unknown)
#

# Display offset up + toward the wall face, scale 0.6 (mirrors zombies/wallbuys/place_at + tp)
$summon minecraft:item_display ^ ^0.5 ^-0.49 {Rotation:[$(yaw),0f],billboard:"fixed",item_display:"fixed",Tags:["mgs.editor_display","mgs._ed_new_disp"],transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}
$execute as @n[tag=mgs._ed_new_disp] run loot replace entity @s contents loot mgs:i/$(weapon_id)
tag @e[tag=mgs._ed_new_disp] remove mgs._ed_new_disp

