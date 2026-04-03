
#> mgs:v5.0.0/zombies/pap/on_hover
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/setup_iter {run:"function mgs:v5.0.0/zombies/pap/on_hover",executor:"source"} [ as @n[tag=mgs.pap_new] ]
#

execute store result score #pap_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.pap.price
execute store result storage mgs:temp _pap_hover.id int 1 run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.pap.id
function mgs:v5.0.0/zombies/pap/lookup_machine with storage mgs:temp _pap_hover
data modify storage smithed.actionbar:input message set value {json:[{"text":"⚙ ","color":"dark_red"},{"storage":"mgs:temp","nbt":"_pap_machine.name","color":"gold","interpret":true},[{"text":" - ","color":"gray"}, {"translate":"mgs.cost_2"}],{"score":{"name":"#pap_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gray"}, {"translate":"mgs.points_2"}]],priority:'notification',freeze:5}
function #smithed.actionbar:message

