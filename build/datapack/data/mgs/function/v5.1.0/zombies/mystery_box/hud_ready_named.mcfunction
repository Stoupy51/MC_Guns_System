
#> mgs:v5.1.0/zombies/mystery_box/hud_ready_named
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/mystery_box/hover_at_box
#

data modify storage smithed.actionbar:input message set value {json:[{"text":"🎲 ","color":"light_purple"},{"translate":"mgs.pick_up","color":"green"},{"storage":"mgs:temp","nbt":"_mb_hover_name","interpret":true}],priority:"conditional",freeze:5}
function #smithed.actionbar:message

