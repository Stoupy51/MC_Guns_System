
#> mgs:v5.4.1/kicks/tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.4.1/player/tick
#			mgs:v5.4.1/dialog/close_then
#

execute if score @s mgs.special.deadshot matches 1 run function mgs:v5.4.1/kicks/apply_ds
execute unless score @s mgs.special.deadshot matches 1 run function mgs:v5.4.1/kicks/apply
scoreboard players remove @s mgs.kick 1

