
#> mgs:v5.4.0/zombies/arrival/land
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/arrival/instant
#			mgs:v5.4.0/zombies/portal_strike
#

execute if data entity @s data.walk_to run data modify entity @n[tag=mgs.zb_new_root] data.walk_to set from entity @s data.walk_to
execute if data entity @s data.walk_to as @n[tag=mgs.zb_new_root] at @s run function mgs:v5.4.0/zombies/escort/start_to_target
tag @n[tag=mgs.zb_new_root] remove mgs.zb_new_root

