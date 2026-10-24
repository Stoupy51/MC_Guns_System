
#> mgs:v5.2.0/maps/zombies/kino_der_toten/teleporter/on_hover
#
# @executed	as @e[tag=mgs.kino.teleporter]
#
# @within	mgs:v5.2.0/maps/zombies/kino_der_toten/start {run:"function mgs:v5.2.0/maps/zombies/kino_der_toten/teleporter/on_hover",executor:"source"} [ as @e[tag=mgs.kino.teleporter] ]
#

# Run as the player looking at a pad. Whole seconds left of the timer of the current state, rounded up.
scoreboard players operation #kino_tp_sec mgs.data = #kino_tp_timer mgs.data
execute if score #kino_tp_state mgs.data matches 6 run scoreboard players operation #kino_tp_sec mgs.data = #kino_tp_cd mgs.data
scoreboard players add #kino_tp_sec mgs.data 19
scoreboard players operation #kino_tp_sec mgs.data /= #20 mgs.data

execute if score #kino_tp_state mgs.data matches 0 if entity @n[tag=bs.interaction.target,tag=mgs.kino.teleporter_theater] run data modify storage smithed.actionbar:input message set value {json:[{"text":"⚡ ","color":"white"},{"translate":"mgs.teleporter","fallback":"Teleporter","color":"yellow"},[{"text":" - ","color":"gray"}, {"translate":"mgs.click_to_start_the_link","fallback":"Click to start the link"}]],priority:"conditional",freeze:5}
execute if score #kino_tp_state mgs.data matches 0 if entity @n[tag=bs.interaction.target,tag=mgs.kino.teleporter_lobby] run data modify storage smithed.actionbar:input message set value {json:[{"text":"⚡ ","color":"white"},{"translate":"mgs.teleporter","fallback":"Teleporter","color":"yellow"},{"translate":"mgs.start_the_link_at_the_theater_pad","fallback":" - Start the link at the theater pad","color":"gray"}],priority:"conditional",freeze:5}
execute if score #kino_tp_state mgs.data matches 1 if entity @n[tag=bs.interaction.target,tag=mgs.kino.teleporter_theater] run data modify storage smithed.actionbar:input message set value {json:[{"text":"⚡ ","color":"white"},{"translate":"mgs.teleporter","fallback":"Teleporter","color":"yellow"},[{"text":" - ","color":"gold"}, {"translate":"mgs.waiting_for_the_lobby_pad","fallback":"Waiting for the lobby pad"}]],priority:"conditional",freeze:5}
execute if score #kino_tp_state mgs.data matches 1 if entity @n[tag=bs.interaction.target,tag=mgs.kino.teleporter_lobby] run data modify storage smithed.actionbar:input message set value {json:[{"text":"⚡ ","color":"white"},{"translate":"mgs.teleporter","fallback":"Teleporter","color":"yellow"},[{"text":" - ","color":"green"}, {"translate":"mgs.click_to_complete_the_link","fallback":"Click to complete the link"}]],priority:"conditional",freeze:5}
execute if score #kino_tp_state mgs.data matches 2 if entity @n[tag=bs.interaction.target,tag=mgs.kino.teleporter_theater] run data modify storage smithed.actionbar:input message set value {json:[{"text":"⚡ ","color":"white"},{"translate":"mgs.teleporter","fallback":"Teleporter","color":"yellow"},[{"text":" - ","color":"green"}, {"translate":"mgs.linked_click_to_teleport","fallback":"Linked, click to teleport"}]],priority:"conditional",freeze:5}
execute if score #kino_tp_state mgs.data matches 2 if entity @n[tag=bs.interaction.target,tag=mgs.kino.teleporter_lobby] run data modify storage smithed.actionbar:input message set value {json:[{"text":"⚡ ","color":"white"},{"translate":"mgs.teleporter","fallback":"Teleporter","color":"yellow"},[{"text":" - ","color":"green"}, {"translate":"mgs.linked_use_the_theater_pad","fallback":"Linked, use the theater pad"}]],priority:"conditional",freeze:5}
execute if score #kino_tp_state mgs.data matches 3 run data modify storage smithed.actionbar:input message set value {json:[{"text":"⚡ ","color":"white"},{"translate":"mgs.teleporter","fallback":"Teleporter","color":"yellow"},[{"text":" - ","color":"aqua"}, {"translate":"mgs.teleporting","fallback":"Teleporting..."}]],priority:"conditional",freeze:5}
execute if score #kino_tp_state mgs.data matches 4 run data modify storage smithed.actionbar:input message set value {json:[{"text":"⚡ ","color":"white"},{"translate":"mgs.teleporter","fallback":"Teleporter","color":"yellow"},[{"text":" - ","color":"aqua"}, {"translate":"mgs.in_use","fallback":"In use: "}],{"score":{"name":"#kino_tp_sec","objective":"mgs.data"},"color":"white"},{"text":"s","color":"gray"}],priority:"conditional",freeze:5}
execute if score #kino_tp_state mgs.data matches 5 run data modify storage smithed.actionbar:input message set value {json:[{"text":"⚡ ","color":"white"},{"translate":"mgs.teleporter","fallback":"Teleporter","color":"yellow"},[{"text":" - ","color":"aqua"}, {"translate":"mgs.returning","fallback":"Returning: "}],{"score":{"name":"#kino_tp_sec","objective":"mgs.data"},"color":"white"},{"text":"s","color":"gray"}],priority:"conditional",freeze:5}
execute if score #kino_tp_state mgs.data matches 6 run data modify storage smithed.actionbar:input message set value {json:[{"text":"⚡ ","color":"white"},{"translate":"mgs.teleporter","fallback":"Teleporter","color":"yellow"},[{"text":" - ","color":"red"}, {"translate":"mgs.recharging","fallback":"Recharging: "}],{"score":{"name":"#kino_tp_sec","objective":"mgs.data"},"color":"white"},{"text":"s","color":"gray"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message

