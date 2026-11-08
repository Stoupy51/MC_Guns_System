
#> mgs:v5.4.1/zombies/spawns/check_box
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/spawns/check_boxes [ as @e[type=minecraft:marker,tag=...] ]
#

tag @s remove mgs.spawn_abox_ok
function mgs:v5.4.1/zombies/spawns/test_box with entity @s data.abox

