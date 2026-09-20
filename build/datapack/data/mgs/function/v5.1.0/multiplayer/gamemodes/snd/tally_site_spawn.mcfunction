
#> mgs:v5.1.0/multiplayer/gamemodes/snd/tally_site_spawn
#
# @executed	as @e[tag=...,limit=1,sort=nearest]
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/tally_site [ as @e[tag=...,limit=1,sort=nearest] ]
#

execute if entity @s[tag=mgs.spawn_red] run scoreboard players add #snd_near_red mgs.data 1
execute if entity @s[tag=mgs.spawn_blue] run scoreboard players add #snd_near_blue mgs.data 1

