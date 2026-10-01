
#> mgs:v5.1.0/zombies/traps/cooldown_tick
#
# @executed	as @e[type=minecraft:marker,tag=mgs.trap_center,scores={mgs.zb.trap.cd=1..}]
#
# @within	mgs:v5.1.0/zombies/game_tick [ as @e[type=minecraft:marker,tag=mgs.trap_center,scores={mgs.zb.trap.cd=1..}] ]
#

# A cooldown above its max is a stale absolute deadline from older versions: clear it.
execute if score @s mgs.zb.trap.cd > @s mgs.zb.trap.cd_max run scoreboard players set @s mgs.zb.trap.cd 0

scoreboard players operation @s mgs.zb.trap.cd -= #tick_delta mgs.data

