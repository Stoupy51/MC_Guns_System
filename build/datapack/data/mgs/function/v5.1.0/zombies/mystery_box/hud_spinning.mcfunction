
#> mgs:v5.1.0/zombies/mystery_box/hud_spinning
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/mystery_box/hover_at_box
#

data modify storage smithed.actionbar:input message set value {json:["🎲 ",{"translate":"mgs.mystery_box","color":"light_purple"},{"text":" - ","color":"gray"},{"translate":"mgs.spinning","color":"yellow"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message

## sourceMappingURL=hud_spinning.mcfunction.map
