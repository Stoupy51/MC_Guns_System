
#> mgs:v5.1.0/player/flash_tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/tick
#

# @s = a player whose burst has been held long enough to have faded out
function mgs:v5.1.0/player/flash_clear
scoreboard players reset @s mgs.flash_off

