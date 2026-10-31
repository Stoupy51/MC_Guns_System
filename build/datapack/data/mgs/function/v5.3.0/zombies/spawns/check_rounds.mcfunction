
#> mgs:v5.3.0/zombies/spawns/check_rounds
#
# @within	mgs:v5.3.0/zombies/start_round
#

tag @e[type=minecraft:marker,tag=mgs.spawn_ranged] remove mgs.spawn_round_ok
execute as @e[type=minecraft:marker,tag=mgs.spawn_ranged] if score #zb_round mgs.data >= @s mgs.zb.spawn.rmin if score #zb_round mgs.data <= @s mgs.zb.spawn.rmax run tag @s add mgs.spawn_round_ok

