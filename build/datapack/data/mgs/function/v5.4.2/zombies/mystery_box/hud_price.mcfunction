
#> mgs:v5.4.2/zombies/mystery_box/hud_price
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/mystery_box/hover_at_box
#

data modify storage smithed.actionbar:input message set value {json:["🎲 ",{"translate":"mgs.mystery_box","fallback":"Mystery Box","color":"light_purple"},{"text":" - ","color":"gray"},{"score":{"name":"#zb_mystery_box_price","objective":"mgs.config"},"color":"gold"},[{"text":" ","color":"gold"}, {"translate":"mgs.points_2","fallback":"points"}]],priority:"conditional",freeze:5}
function #smithed.actionbar:message

