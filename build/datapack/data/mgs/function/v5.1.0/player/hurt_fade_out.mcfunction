
#> mgs:v5.1.0/player/hurt_fade_out
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/hurt_sweep
#			mgs:v5.1.0/player/fx_reset
#

# @s = a player with no hurt id applied, #hurt_was = the level whose look the fade starts from
scoreboard players operation @s mgs.hurt_fx = #hurt_was mgs.data
scoreboard players set #hurt_tier mgs.data 0
function mgs:v5.1.0/player/hurt_swap

