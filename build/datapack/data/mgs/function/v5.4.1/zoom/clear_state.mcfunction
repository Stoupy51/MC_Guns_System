
#> mgs:v5.4.1/zoom/clear_state
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/switch/on_weapon_switch
#

playsound mgs:common/lean_out player @s
scoreboard players reset @s mgs.zoom
effect clear @s slowness
function mgs:v5.4.1/zoom/fx_leave

