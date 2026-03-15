
#> mgs:v5.0.0/zombies/perks/on_hover
#
# @within	???
#

execute store result score #pk_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.perk.price
execute store result storage mgs:temp _pk_hover.id int 1 run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.perk.id
function mgs:v5.0.0/zombies/perks/lookup_perk with storage mgs:temp _pk_hover
function mgs:v5.0.0/zombies/perks/get_hover_name
data modify storage smithed.actionbar:input message set value {json:[{"text":"🥤 ","color":"dark_purple"},{"storage":"mgs:temp","nbt":"_pk_hover_name","color":"light_purple","interpret":true},[{"text":" - ","color":"gray"}, {"translate":"mgs.cost_2"}],{"score":{"name":"#pk_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gray"}, {"translate":"mgs.points_2"}]],priority:'notification',freeze:5}
function #smithed.actionbar:message

