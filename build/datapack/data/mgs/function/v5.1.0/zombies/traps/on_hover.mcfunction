
#> mgs:v5.1.0/zombies/traps/on_hover
#
# @executed	as @e[tag=mgs._trap_new_bs]
#
# @within	mgs:v5.1.0/zombies/traps/setup_iter {run:"function mgs:v5.1.0/zombies/traps/on_hover",executor:"source"} [ as @e[tag=mgs._trap_new_bs] ]
#

execute store result score #trap_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.trap.price
execute store result score #trap_type mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.trap.type

# json[0] is a nested list so the per-type overwrites below still swap emoji AND name in one write.
# Its neutral "" head keeps the emoji white without tinting the siblings, which carry their own colors.
data modify storage smithed.actionbar:input message set value {json:[["",{"text":"⚠ ","color":"white"},{"translate":"mgs.trap","color":"red"}],[{"text":" - ","color":"gray"}, {"translate":"mgs.cost_2"}],{"score":{"name":"#trap_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gray"}, {"translate":"mgs.points_2"}]],priority:"conditional",freeze:5}
execute if score #trap_type mgs.data matches 0 run data modify storage smithed.actionbar:input message.json[0] set value ["",{"text":"🔥 ","color":"white"},{"translate":"mgs.fire_trap","color":"red"}]
execute if score #trap_type mgs.data matches 1 run data modify storage smithed.actionbar:input message.json[0] set value ["",{"text":"⚡ ","color":"white"},{"translate":"mgs.electric_trap","color":"aqua"}]
execute if score #trap_type mgs.data matches 2 run data modify storage smithed.actionbar:input message.json[0] set value ["",{"text":"🔫 ","color":"white"},{"translate":"mgs.turret_trap","color":"gold"}]
function #smithed.actionbar:message

## sourceMappingURL=on_hover.mcfunction.map
