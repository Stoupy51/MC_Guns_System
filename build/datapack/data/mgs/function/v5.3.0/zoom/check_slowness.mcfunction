
#> mgs:v5.3.0/zoom/check_slowness
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zoom/main
#

# No gun: the vanilla crosshair sprite is blank, so the shader draws a copy of it.
function mgs:v5.3.0/zoom/crosshair_base

# Switched away from a gun while zoomed: remove the slowness.
execute unless score @s mgs.zoom matches 1 run return fail
playsound mgs:common/lean_out player @s
scoreboard players reset @s mgs.zoom
effect clear @s slowness
function mgs:v5.3.0/zoom/fx_leave

