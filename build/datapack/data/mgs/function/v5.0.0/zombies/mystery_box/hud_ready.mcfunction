
#> mgs:v5.0.0/zombies/mystery_box/hud_ready
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.0.0/zombies/mystery_box/on_hover
#

data modify storage smithed.actionbar:input message set value {json:[[{"text":"🎲 ","color":"light_purple"}, {"translate":"mgs.mystery_box"}],{"text":" - ","color":"gray"},{"translate":"mgs.click_to_collect","color":"green"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message

