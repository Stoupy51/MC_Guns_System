
#> mgs:v5.0.0/zombies/traps/active_tick
#
# @executed	as @e[tag=mgs.trap_center,scores={mgs.zb.trap.timer=1..}] & at @s
#
# @within	mgs:v5.0.0/zombies/game_tick [ as @e[tag=mgs.trap_center,scores={mgs.zb.trap.timer=1..}] & at @s ]
#

# @s = trap center marker, at @s position

# Apply damage based on trap type
execute store result storage mgs:temp _trap_tick.rx int 1 run scoreboard players get @s mgs.zb.trap.rx
execute store result storage mgs:temp _trap_tick.ry int 1 run scoreboard players get @s mgs.zb.trap.ry
execute store result storage mgs:temp _trap_tick.rz int 1 run scoreboard players get @s mgs.zb.trap.rz

scoreboard players operation #trap_sx mgs.data = @s mgs.zb.trap.rx
scoreboard players operation #trap_sy mgs.data = @s mgs.zb.trap.ry
scoreboard players operation #trap_sz mgs.data = @s mgs.zb.trap.rz
scoreboard players operation #trap_sx mgs.data += #trap_sx mgs.data
scoreboard players operation #trap_sy mgs.data += #trap_sy mgs.data
scoreboard players operation #trap_sz mgs.data += #trap_sz mgs.data
execute store result storage mgs:temp _trap_tick.sx int 1 run scoreboard players get #trap_sx mgs.data
execute store result storage mgs:temp _trap_tick.sy int 1 run scoreboard players get #trap_sy mgs.data
execute store result storage mgs:temp _trap_tick.sz int 1 run scoreboard players get #trap_sz mgs.data

execute if score @s mgs.zb.trap.type matches 0 run function mgs:v5.0.0/zombies/traps/damage_fire with storage mgs:temp _trap_tick
execute if score @s mgs.zb.trap.type matches 1 run function mgs:v5.0.0/zombies/traps/damage_electric with storage mgs:temp _trap_tick

# Particles based on type
execute if score @s mgs.zb.trap.type matches 0 run particle minecraft:flame ~ ~1 ~ 1.5 0.5 1.5 0.05 10
execute if score @s mgs.zb.trap.type matches 1 run particle minecraft:electric_spark ~ ~1 ~ 1.5 0.5 1.5 0.1 15

# Decrement timer
scoreboard players remove @s mgs.zb.trap.timer 1

# Check if deactivated
execute if score @s mgs.zb.trap.timer matches 0 run scoreboard players operation @s mgs.zb.trap.cd = @s mgs.zb.trap.cd_max

