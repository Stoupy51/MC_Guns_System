
#> mgs:v5.4.2/zombies/mystery_box/hud_ready
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/mystery_box/hover_at_box
#

data modify storage smithed.actionbar:input message set value {json:[{"text":"🎲 ","color":"white"},{"translate":"mgs.mystery_box","fallback":"Mystery Box","color":"light_purple"},{"text":" - ","color":"gray"},{"translate":"mgs.click_to_collect","fallback":"Click to collect!","color":"green"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message

