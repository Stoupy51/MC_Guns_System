
#> mgs:v5.0.0/multiplayer/custom/toggle_entry_vis
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/custom/toggle_vis_rebuild
#

# Read current value and flip
execute store result score #pub mgs.data run data get storage mgs:temp _del_src[0].public
execute if score #pub mgs.data matches 1 run data modify storage mgs:temp _del_src[0].public set value 0b
execute if score #pub mgs.data matches 0 run data modify storage mgs:temp _del_src[0].public set value 1b

