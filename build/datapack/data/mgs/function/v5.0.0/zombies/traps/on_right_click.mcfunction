
#> mgs:v5.0.0/zombies/traps/on_right_click
#
# @within	???
#

# Guard: game must be active
execute unless data storage mgs:zombies game{state:"active"} run return fail

# Check power requirement
execute store result score #trap_power mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.trap.power
execute if score #trap_power mgs.data matches 1 unless score #zb_power mgs.data matches 1 run return run function mgs:v5.0.0/zombies/traps/deny_requires_power

# Get trap ID
execute store result score #trap_id mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.trap.id

# Check if trap is ready (not active, not on cooldown)
scoreboard players set #trap_ready mgs.data 0
execute as @e[tag=mgs.trap_center] if score @s mgs.zb.trap.id = #trap_id mgs.data if score @s mgs.zb.trap.timer matches 0 if score @s mgs.zb.trap.cd matches 0 run scoreboard players set #trap_ready mgs.data 1
execute unless score #trap_ready mgs.data matches 1 run return run function mgs:v5.0.0/zombies/traps/deny_not_ready

# Check price
execute store result score #trap_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.trap.price
execute unless score @s mgs.zb.points >= #trap_price mgs.data run return run function mgs:v5.0.0/zombies/traps/deny_not_enough_points

# Deduct points
scoreboard players operation @s mgs.zb.points -= #trap_price mgs.data

# Activate trap (set timer = duration on the marker)
execute as @e[tag=mgs.trap_center] if score @s mgs.zb.trap.id = #trap_id mgs.data run scoreboard players operation @s mgs.zb.trap.timer = @s mgs.zb.trap.dur

# Announce
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.trap_activated_for","color":"gold"},{"score":{"name":"#trap_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gold"}, {"translate":"mgs.points_2"}]]
function mgs:v5.0.0/zombies/feedback/sound_announce

