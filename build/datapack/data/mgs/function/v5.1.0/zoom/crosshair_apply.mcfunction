
#> mgs:v5.1.0/zoom/crosshair_apply
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zoom/crosshair_spread
#			mgs:v5.1.0/zoom/crosshair_base
#

# @s = any player, #spread = the level to show
execute unless score @s mgs.cross_to matches -2147483648.. run return run function mgs:v5.1.0/zoom/crosshair_first
execute if score @s mgs.cross_to = #spread mgs.data run return 0
function mgs:v5.1.0/zoom/crosshair_swap

