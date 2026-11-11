
#> mgs:v5.4.2/zombies/mystery_box/hud_spinning
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/mystery_box/hover_at_box
#

data modify storage smithed.actionbar:input message set value {json:["🎲 ",{"translate":"mgs.mystery_box","fallback":"Mystery Box","color":"light_purple"},{"text":" - ","color":"gray"},{"translate":"mgs.spinning","fallback":"Spinning...","color":"yellow"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message

