
#> mgs:v5.4.1/player/stamina_init
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/player/stamina_tick
#

scoreboard players set @s mgs.stam_max 300
scoreboard players operation @s mgs.stam_max += @s mgs.stam_bonus
scoreboard players operation @s mgs.stam = @s mgs.stam_max
scoreboard players set @s mgs.stam_out 0
scoreboard players set @s mgs.stam_rest 0
scoreboard players set @s mgs.stam_swim 0
scoreboard players set @s mgs.stam_seen 1

# Assume the most leftover saturation from before the game (the stop refill), so the first at-target ticks burn it off.
scoreboard players set @s mgs.stam_sat 500

