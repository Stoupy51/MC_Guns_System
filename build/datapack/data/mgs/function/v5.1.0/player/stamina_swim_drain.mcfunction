
#> mgs:v5.1.0/player/stamina_swim_drain
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/stamina_tick
#

scoreboard players add @s mgs.stam_swim 1
execute if score @s mgs.stam_swim matches 5.. run scoreboard players set @s mgs.stam_swim 0
execute if score @s mgs.stam_swim matches 0 run scoreboard players remove @s mgs.stam 2

