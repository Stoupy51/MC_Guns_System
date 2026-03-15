
#> mgs:v5.0.0/zombies/traps/on_hover
#
# @within	???
#

execute store result score #trap_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.trap.price
data modify storage smithed.actionbar:input message set value {json:[[{"text":"⚠ ","color":"red"}, {"translate":"mgs.trap"}],[{"text":" - ","color":"gray"}, {"translate":"mgs.cost_2"}],{"score":{"name":"#trap_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gray"}, {"translate":"mgs.points_2"}]],priority:'notification',freeze:5}
function #smithed.actionbar:message

