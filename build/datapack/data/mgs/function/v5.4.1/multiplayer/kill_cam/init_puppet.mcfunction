
#> mgs:v5.4.1/multiplayer/kill_cam/init_puppet
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/kill_cam/drive_puppet [ at 006d6773-0000-0000-0000-000000006b63 ]
#

data merge entity @s {NoGravity:true,immovable:true,hide_description:true,Invulnerable:true,Tags:["mgs.kc_puppet","mgs.kill_cam","mgs.multiplayer_entity","mgs.kc_new"]}
scoreboard players operation @s mgs.mp.kc_id = #kc_sid mgs.data
execute as @a if score @s bs.id = #kc_sid mgs.data run function mgs:v5.4.1/multiplayer/kill_cam/dress_puppet
tag @s remove mgs.kc_new
function mgs:v5.4.1/multiplayer/kill_cam/move_puppet

