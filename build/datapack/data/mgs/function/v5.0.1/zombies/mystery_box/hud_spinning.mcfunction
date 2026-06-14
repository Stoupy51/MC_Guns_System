
#> mgs:v5.0.1/zombies/mystery_box/hud_spinning
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.0.1/zombies/mystery_box/hover_at_box
#

data modify storage smithed.actionbar:input message set value {json:[[{"text":"🎲 ","color":"light_purple"}, {"translate":"mgs.mystery_box"}],{"text":" - ","color":"gray"},{"translate":"mgs.spinning","color":"yellow"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message

