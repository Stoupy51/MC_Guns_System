
#> mgs:v5.4.1/multiplayer/kill_cam/move_puppet
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/kill_cam/drive_puppet [ at 006d6773-0000-0000-0000-000000006b63 ]
#			mgs:v5.4.1/multiplayer/kill_cam/init_puppet
#

tag @s add mgs.kc_seen
tp @s ~ ~ ~ ~ ~
execute if score #kc_sneak mgs.data matches 1 unless entity @s[tag=mgs.kc_crouch] run data modify entity @s pose set value "crouching"
execute if score #kc_sneak mgs.data matches 0 if entity @s[tag=mgs.kc_crouch] run data modify entity @s pose set value "standing"
execute if score #kc_sneak mgs.data matches 1 run tag @s add mgs.kc_crouch
execute if score #kc_sneak mgs.data matches 0 run tag @s remove mgs.kc_crouch

