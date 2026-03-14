
#> mgs:v5.0.0/zombies/mystery_box/hud_spinning
#
# @within	mgs:v5.0.0/zombies/mystery_box/on_hover
#

data modify storage smithed.actionbar:input message set value {json:[{"translate":"mgs.mystery_box","color":"light_purple"},{"text":" - ","color":"gray"},{"translate":"mgs.spinning","color":"yellow"}],priority:'notification',freeze:5}
function #smithed.actionbar:message

