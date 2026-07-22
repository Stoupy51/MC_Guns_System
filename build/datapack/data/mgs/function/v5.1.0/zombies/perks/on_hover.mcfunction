
#> mgs:v5.1.0/zombies/perks/on_hover
#
# @executed	as @n[tag=mgs.pk_new]
#
# @within	mgs:v5.1.0/zombies/perks/setup_iter {run:"function mgs:v5.1.0/zombies/perks/on_hover",executor:"source"} [ as @n[tag=mgs.pk_new] ]
#

execute store result storage mgs:temp _pk_hover.id int 1 run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.perk.id
function mgs:v5.1.0/zombies/perks/lookup_perk with storage mgs:temp _pk_hover
function mgs:v5.1.0/zombies/perks/get_hover_name
function mgs:v5.1.0/zombies/perks/read_price with storage mgs:temp _pk_data
execute unless score #pk_partial mgs.data matches 1.. run data modify storage smithed.actionbar:input message set value {json:[{"text":"🥤 ","color":"dark_purple"},{"storage":"mgs:temp","nbt":"_pk_hover_name","color":"light_purple","interpret":true},[{"text":" - ","color":"gray"}, {"translate":"mgs.cost_2"}],{"score":{"name":"#pk_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gray"}, {"translate":"mgs.points_2"}]],priority:"conditional",freeze:5}
execute if score #pk_partial mgs.data matches 1.. run data modify storage smithed.actionbar:input message set value {json:[{"text":"🥤 ","color":"dark_purple"},{"storage":"mgs:temp","nbt":"_pk_hover_name","color":"light_purple","interpret":true},[{"text":" - ","color":"gray"}, {"translate":"mgs.chip_in"}],{"score":{"name":"#pk_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gray"}, {"translate":"mgs.points_2"}, "  ("],{"score":{"name":"#pk_paid","objective":"mgs.data"},"color":"green"},{"text":"/","color":"gray"},{"score":{"name":"#pk_total","objective":"mgs.data"},"color":"yellow"},{"text":")","color":"gray"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message

