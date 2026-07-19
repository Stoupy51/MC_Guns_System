
#> mgs:v5.1.0/zombies/traps/cooldown_tick
#
# @executed	as @e[type=minecraft:marker,tag=mgs.trap_center,scores={mgs.zb.trap.cd=1..}]
#
# @within	mgs:v5.1.0/zombies/game_tick [ as @e[type=minecraft:marker,tag=mgs.trap_center,scores={mgs.zb.trap.cd=1..}] ]
#

# A countdown can never exceed its own maximum, so anything larger is a stale absolute deadline
# left by the old #real_tick scheme — clear it rather than make players wait out a dead timestamp.
execute if score @s mgs.zb.trap.cd > @s mgs.zb.trap.cd_max run scoreboard players set @s mgs.zb.trap.cd 0

scoreboard players operation @s mgs.zb.trap.cd -= #tick_delta mgs.data

