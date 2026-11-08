
#> mgs:v5.4.1/zombies/mystery_box/hud_moving
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/mystery_box/on_hover
#

data modify storage smithed.actionbar:input message set value {json:["🎲 ",{"translate":"mgs.mystery_box","fallback":"Mystery Box","color":"light_purple"},{"text":" - ","color":"gray"},{"translate":"mgs.moving","fallback":"Moving...","color":"yellow"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message

