
#> mgs:v5.0.1/player/stamina_init
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/player/stamina_tick
#

scoreboard players set @s mgs.stam 100
scoreboard players set @s mgs.stam_out 0
scoreboard players set @s mgs.stam_rest 0
scoreboard players operation @s mgs.stam_prev = @s mgs.sprint
scoreboard players set @s mgs.stam_seen 1

