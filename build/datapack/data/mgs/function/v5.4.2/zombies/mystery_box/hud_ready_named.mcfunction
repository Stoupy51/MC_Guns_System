
#> mgs:v5.4.2/zombies/mystery_box/hud_ready_named
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/mystery_box/hover_at_box
#

data modify storage smithed.actionbar:input message set value {json:["🎲 ",{"translate":"mgs.pick_up","fallback":"Pick-up ","color":"green"},{"storage":"mgs:temp","nbt":"_mb_hover_name","interpret":true,"color":"light_purple"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message

