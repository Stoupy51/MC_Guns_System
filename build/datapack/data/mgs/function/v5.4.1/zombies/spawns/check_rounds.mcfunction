
#> mgs:v5.4.1/zombies/spawns/check_rounds
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/start_round
#

tag @e[type=minecraft:marker,tag=mgs.spawn_ranged] remove mgs.spawn_round_ok
execute as @e[type=minecraft:marker,tag=mgs.spawn_ranged] if score #zb_round mgs.data >= @s mgs.zb.spawn.rmin if score #zb_round mgs.data <= @s mgs.zb.spawn.rmax run tag @s add mgs.spawn_round_ok

