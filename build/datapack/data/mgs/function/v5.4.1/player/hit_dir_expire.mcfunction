
#> mgs:v5.4.1/player/hit_dir_expire
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.4.1/player/tick
#			mgs:v5.4.1/dialog/close_then
#

# @s = a player whose arc has faded out
function mgs:v5.4.1/player/hit_dir_clear
scoreboard players reset @s mgs.hit_dir_off

