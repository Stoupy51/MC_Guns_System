
#> mgs:v5.1.0/zombies/mystery_box/hud_ready
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/mystery_box/hover_at_box
#

data modify storage smithed.actionbar:input message set value {json:[[{"text":"🎲 ","color":"light_purple"}, {"translate":"mgs.mystery_box"}],{"text":" - ","color":"gray"},{"translate":"mgs.click_to_collect","color":"green"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message

