
#> mgs:v5.1.0/grenade/stick_to_entity
#
# @executed	at @s
#
# @within	mgs:v5.1.0/grenade/on_stick
#

scoreboard players add #semtex_id mgs.data 1

scoreboard players operation @s mgs.stuck_id = #semtex_id mgs.data
execute positioned ~ ~-1 ~ run scoreboard players operation @n[type=!#mgs:ignore,distance=..2,tag=!mgs.grenade,tag=!mgs.slow_bullet,tag=!global.ignore.kill,tag=!global.ignore,nbt=!{Invulnerable:true}] mgs.stuck_id = #semtex_id mgs.data

tag @s add mgs.stuck_to_entity

