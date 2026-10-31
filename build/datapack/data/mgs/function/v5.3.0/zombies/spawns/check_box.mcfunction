
#> mgs:v5.3.0/zombies/spawns/check_box
#
# @executed	as @e[type=minecraft:marker,tag=...]
#
# @within	mgs:v5.3.0/zombies/spawns/check_boxes [ as @e[type=minecraft:marker,tag=...] ]
#

tag @s remove mgs.spawn_abox_ok
function mgs:v5.3.0/zombies/spawns/test_box with entity @s data.abox

