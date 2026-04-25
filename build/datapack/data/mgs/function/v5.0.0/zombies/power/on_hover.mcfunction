
#> mgs:v5.0.0/zombies/power/on_hover
#
# @executed	as @e[tag=_pw_new]
#
# @within	mgs:v5.0.0/zombies/power/place_at {run:"function mgs:v5.0.0/zombies/power/on_hover",executor:"source"} [ as @e[tag=_pw_new] ]
#

data modify storage smithed.actionbar:input message set value {json:[[{"text":"⚡ ","color":"yellow"}, {"translate":"mgs.power_switch"}]],priority:"conditional",freeze:5}
function #smithed.actionbar:message

