
#> mgs:v5.1.0/zombies/mystery_box/hud_moving
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.1.0/zombies/mystery_box/on_hover
#

data modify storage smithed.actionbar:input message set value {json:["🎲 ",{"translate":"mgs.mystery_box","color":"light_purple"},{"text":" - ","color":"gray"},{"translate":"mgs.moving","color":"yellow"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message

