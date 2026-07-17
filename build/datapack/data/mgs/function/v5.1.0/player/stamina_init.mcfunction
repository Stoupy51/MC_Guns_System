
#> mgs:v5.1.0/player/stamina_init
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/stamina_tick
#

scoreboard players set @s mgs.stam_max 200
scoreboard players operation @s mgs.stam_max += @s mgs.stam_bonus
scoreboard players operation @s mgs.stam = @s mgs.stam_max
scoreboard players set @s mgs.stam_out 0
scoreboard players set @s mgs.stam_rest 0
scoreboard players set @s mgs.stam_seen 1

# Assume leftover invisible saturation from before the game (e.g. the game-stop refill pin),
# so the first at-target ticks verify and burn it off
scoreboard players set @s mgs.stam_dirty 1

