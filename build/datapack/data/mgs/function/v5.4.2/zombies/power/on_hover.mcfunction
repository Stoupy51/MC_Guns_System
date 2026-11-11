
#> mgs:v5.4.2/zombies/power/on_hover
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/power/place_at {run:"function mgs:v5.4.2/zombies/power/on_hover",executor:"source"} [ as @e[tag=_pw_new] ]
#

data modify storage smithed.actionbar:input message set value {json:[{"text":"⚡ ","color":"white"},{"translate":"mgs.power_switch","fallback":"Power Switch","color":"yellow"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message

