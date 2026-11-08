
#> mgs:v5.4.1/player/hurt_fade_out
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/player/hurt_sweep
#			mgs:v5.4.1/player/fx_reset
#

# @s = a player with no hurt id applied, #hurt_was = the level whose look the fade starts from
scoreboard players operation @s mgs.hurt_fx = #hurt_was mgs.data
scoreboard players set #hurt_tier mgs.data 0
function mgs:v5.4.1/player/hurt_swap

