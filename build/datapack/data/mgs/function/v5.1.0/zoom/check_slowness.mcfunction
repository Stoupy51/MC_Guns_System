
#> mgs:v5.1.0/zoom/check_slowness
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zoom/main
#

# Not holding a gun: the vanilla crosshair sprite is blanked, so show the static base one
function mgs:v5.1.0/zoom/crosshair_base

# If player was zooming and switched slot so no longer holding a gun, remove slowness effect
execute unless score @s mgs.zoom matches 1 run return fail
playsound mgs:common/lean_out player @s
scoreboard players reset @s mgs.zoom
effect clear @s slowness
function mgs:v5.1.0/zoom/fx_leave

