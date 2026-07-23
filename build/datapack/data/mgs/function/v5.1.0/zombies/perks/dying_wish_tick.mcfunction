
#> mgs:v5.1.0/zombies/perks/dying_wish_tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

particle minecraft:crit ~ ~1 ~ 0.4 0.6 0.4 0.05 4 force @a[distance=..24]
scoreboard players remove @s mgs.zb.dw_timer 1
execute if score @s mgs.zb.dw_timer matches ..0 run function mgs:v5.1.0/zombies/perks/dying_wish_end

