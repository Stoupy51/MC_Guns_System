
#> mgs:v5.1.0/zombies/traps/on_right_click
#
# @executed	as @e[tag=mgs._trap_new_bs]
#
# @within	mgs:v5.1.0/zombies/traps/setup_iter {run:"function mgs:v5.1.0/zombies/traps/on_right_click",executor:"source"} [ as @e[tag=mgs._trap_new_bs] ]
#

execute unless data storage mgs:zombies game{state:"active"} run return fail

execute store result score #trap_power mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.trap.power
execute if score #trap_power mgs.data matches 1 unless score #zb_power mgs.data matches 1 run return run function mgs:v5.1.0/zombies/deny/message {msg:'{"translate":"mgs.this_trap_requires_power","color":"red"}'}

execute store result score #trap_id mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.trap.id

# Neither active nor on cooldown.
scoreboard players set #trap_ready mgs.data 0
execute as @e[type=minecraft:marker,tag=mgs.trap_center] if score @s mgs.zb.trap.id = #trap_id mgs.data if score @s mgs.zb.trap.timer matches 0 if score @s mgs.zb.trap.cd matches ..0 run scoreboard players set #trap_ready mgs.data 1
execute unless score #trap_ready mgs.data matches 1 run return run function mgs:v5.1.0/zombies/deny/message {msg:'{"translate":"mgs.trap_is_on_cooldown_and_not_ready_yet","color":"yellow"}'}

execute store result score #trap_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.trap.price
execute unless score @s mgs.zb.points >= #trap_price mgs.data run return run function mgs:v5.1.0/zombies/deny/not_enough_points {score:"#trap_price",obj:"mgs.data"}

scoreboard players operation @s mgs.zb.points -= #trap_price mgs.data

# The marker's timer is set to the duration.
execute as @e[type=minecraft:marker,tag=mgs.trap_center] if score @s mgs.zb.trap.id = #trap_id mgs.data run scoreboard players operation @s mgs.zb.trap.timer = @s mgs.zb.trap.dur

# Read at deactivation.
execute unless score @s mgs.special.timeslip matches 1.. as @e[type=minecraft:marker,tag=mgs.trap_center] if score @s mgs.zb.trap.id = #trap_id mgs.data run scoreboard players set @s mgs.zb.trap.timeslip 0
execute if score @s mgs.special.timeslip matches 1.. as @e[type=minecraft:marker,tag=mgs.trap_center] if score @s mgs.zb.trap.id = #trap_id mgs.data run scoreboard players set @s mgs.zb.trap.timeslip 1

tag @a remove mgs.xp_earner
tag @s add mgs.xp_earner
tellraw @a[scores={mgs.zb.in_game=1},tag=!mgs.xp_earner] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.trap_activated_for","color":"gold"},{"score":{"name":"#trap_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gold"}, {"translate":"mgs.points_3"}]]
tellraw @a[tag=mgs.xp_earner] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.trap_activated_for","color":"gold"},{"score":{"name":"#trap_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gold"}, {"translate":"mgs.points_3"}],[" ",{"text":"+2 XP","color":"gold"}]]
execute as @a[tag=mgs.xp_earner] run function mgs:v5.1.0/progression/zb/award_trap
tag @a remove mgs.xp_earner
playsound minecraft:block.note_block.bit ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.6 0.9

