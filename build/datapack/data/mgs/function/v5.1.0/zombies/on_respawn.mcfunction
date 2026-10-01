
#> mgs:v5.1.0/zombies/on_respawn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

scoreboard players set @s mgs.mp.death_count 0

scoreboard players add @s mgs.zb.downs 1

function mgs:v5.1.0/zombies/revive/on_down

