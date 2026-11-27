
#> mgs:v5.4.4/zombies/on_respawn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.4.4/player/tick
#			mgs:v5.4.4/dialog/close_then
#

scoreboard players set @s mgs.mp.death_count 0

scoreboard players add @s mgs.zb.downs 1
scoreboard players add @s mgs.st.zb.downs 1

function mgs:v5.4.4/zombies/revive/on_down

