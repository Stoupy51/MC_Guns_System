
#> mgs:v5.1.0/player/hurt_tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

scoreboard players set #hurt_tier mgs.data 0
execute unless entity @s[gamemode=spectator] if score @s mgs.mp.in_game matches 1 run function mgs:v5.1.0/player/hurt_resolve
execute unless entity @s[gamemode=spectator] if score @s mgs.mi.in_game matches 1 run function mgs:v5.1.0/player/hurt_resolve
execute unless entity @s[gamemode=spectator] if score @s mgs.zb.in_game matches 1 run function mgs:v5.1.0/player/hurt_resolve
execute if score @s mgs.hurt_fx = #hurt_tier mgs.data run return 0
function mgs:v5.1.0/player/hurt_swap

