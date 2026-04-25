
#> mgs:v5.0.0/zombies/mystery_box/hud_price
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.0.0/zombies/mystery_box/on_hover
#

data modify storage smithed.actionbar:input message set value {json:[[{"text":"🎲 ","color":"light_purple"}, {"translate":"mgs.mystery_box"}],{"text":" - ","color":"gray"},[{"text":"950 ","color":"gold"}, {"translate":"mgs.points_2"}]],priority:"conditional",freeze:5}
function #smithed.actionbar:message

