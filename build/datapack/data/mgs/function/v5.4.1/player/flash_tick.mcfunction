
#> mgs:v5.4.1/player/flash_tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.4.1/player/tick
#			mgs:v5.4.1/dialog/close_then
#

# @s = a player whose burst has been held long enough to have faded out
function mgs:v5.4.1/player/flash_clear
scoreboard players reset @s mgs.flash_off

