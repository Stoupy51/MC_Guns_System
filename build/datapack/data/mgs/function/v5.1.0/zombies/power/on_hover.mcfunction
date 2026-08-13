
#> mgs:v5.1.0/zombies/power/on_hover
#
# @executed	as @e[tag=_pw_new]
#
# @within	mgs:v5.1.0/zombies/power/place_at {run:"function mgs:v5.1.0/zombies/power/on_hover",executor:"source"} [ as @e[tag=_pw_new] ]
#

data modify storage smithed.actionbar:input message set value {json:[{"text":"⚡ ","color":"white"},{"translate":"mgs.power_switch","color":"yellow"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message

