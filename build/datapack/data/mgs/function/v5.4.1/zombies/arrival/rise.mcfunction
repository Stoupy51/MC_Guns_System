
#> mgs:v5.4.1/zombies/arrival/rise
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/arrival/floor
#			mgs:v5.4.1/zombies/arrival/ceiling
#

tag @n[tag=mgs.zb_new_root] add mgs.zb_rising
scoreboard players operation @n[tag=mgs.zb_new_root] mgs.zb.rise_tick = @s mgs.zb.rise_tick
scoreboard players operation @n[tag=mgs.zb_new_root] mgs.zb.rise_step = #zb_rise_step mgs.data
execute if data entity @s data.walk_to run data modify entity @n[tag=mgs.zb_new_root] data.walk_to set from entity @s data.walk_to
tag @n[tag=mgs.zb_new_root] remove mgs.zb_new_root

