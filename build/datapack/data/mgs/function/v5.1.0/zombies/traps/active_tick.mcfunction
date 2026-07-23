
#> mgs:v5.1.0/zombies/traps/active_tick
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/game_tick [ at @s ]
#

# @s = trap center marker, at @s position

# Apply damage based on trap type
data modify storage mgs:temp _trap_tick set value {rx:0,ry:0,rz:0,sx:0,sy:0,sz:0}
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

execute if score @s mgs.zb.trap.type matches 0 run function mgs:v5.1.0/zombies/traps/damage_fire with storage mgs:temp _trap_tick
execute if score @s mgs.zb.trap.type matches 1 run function mgs:v5.1.0/zombies/traps/damage_electric with storage mgs:temp _trap_tick

# Turret: fire a shot every 5 ticks at the nearest zombie in range
scoreboard players operation #turret_mod mgs.data = @s mgs.zb.trap.timer
scoreboard players operation #turret_mod mgs.data %= #5 mgs.data
execute if score #turret_mod mgs.data matches 0 if score @s mgs.zb.trap.type matches 2 run function mgs:v5.1.0/zombies/traps/turret_fire with storage mgs:temp _trap_tick

# Particles based on type
execute if score @s mgs.zb.trap.type matches 0 run particle minecraft:flame ~ ~1 ~ 1.5 0.5 1.5 0.05 10
execute if score @s mgs.zb.trap.type matches 1 run particle minecraft:electric_spark ~ ~1 ~ 1.5 0.5 1.5 0.1 15
execute if score @s mgs.zb.trap.type matches 2 run particle minecraft:smoke ~ ~1 ~ 0.2 0.2 0.2 0.01 2

# Decrement timer (real-time via #tick_delta, clamped at 0 so the exact-0 checks below still hit)
scoreboard players operation @s mgs.zb.trap.timer -= #tick_delta mgs.data
execute unless score @s mgs.zb.trap.timer matches 0.. run scoreboard players set @s mgs.zb.trap.timer 0

# Check if deactivated: start the cooldown as a countdown. NOT an absolute #real_tick deadline —
# that clock is a stopwatch recreated on every datapack load, so a stored deadline outlived its
# clock and left the trap permanently unusable after any /reload.
execute if score @s mgs.zb.trap.timer matches 0 run scoreboard players operation @s mgs.zb.trap.cd = @s mgs.zb.trap.cd_max

# Timeslip: the activator's trap cooldown is scaled to 75%
execute if score @s mgs.zb.trap.timer matches 0 if score @s mgs.zb.trap.timeslip matches 1 run function mgs:v5.1.0/zombies/traps/apply_timeslip_cd

