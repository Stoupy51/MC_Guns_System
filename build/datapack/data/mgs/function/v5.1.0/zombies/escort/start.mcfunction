
#> mgs:v5.1.0/zombies/escort/start
#
# @executed	as @e[tag=...,limit=24,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/on_stuck_zombie
#			mgs:v5.1.0/zombies/escort/start_to_target
#			mgs:v5.1.0/zombies/escort/update_lure [ as @e[tag=...,limit=2,sort=random] & at @s ]
#			mgs:v5.1.0/zombies/monkey/pull_one
#

# The trader walks and drags the frozen zombie. The team join covers zombies summoned before a mid-game /reload added the team.
tag @s add mgs.zb_escorted
team join mgs.horde @s
data modify entity @s NoAI set value 1b
scoreboard players set @s mgs.zb.escort_ttl 900

# While escorted, stuck_x, stuck_z and stuck_ticks hold a block snapshot and a still counter; detach re-initializes them.
execute store result score @s mgs.zb.stuck_x run data get entity @s Pos[0]
execute store result score @s mgs.zb.stuck_z run data get entity @s Pos[2]
scoreboard players set @s mgs.zb.stuck_ticks 0

# Invisible pathfinding taxi (see the escort module docstring for each NBT choice).
summon minecraft:wandering_trader ~ ~ ~ {Tags:["mgs.zb_escort","mgs.gm_entity","mgs.zb_escort_new","global.ignore","global.ignore.kill"],Silent:1b,Invulnerable:1b,PersistenceRequired:1b,DespawnDelay:0,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",Offers:{Recipes:[]},active_effects:[{id:"minecraft:invisibility",duration:-1,show_particles:0b}]}

team join mgs.horde @n[tag=mgs.zb_escort_new]

# Trader base speed = zombie speed / 0.35 (WanderToPositionGoal modifier). The base, not the effective value:
# a barricade freeze (-1024) would clamp the taxi to 0, and a just-detached zombie's Speed I would read 20% high.
execute store result storage mgs:temp _escort.speed double 0.0028571 run attribute @s minecraft:movement_speed base get 1000
execute as @n[tag=mgs.zb_escort_new] run function mgs:v5.1.0/zombies/escort/set_trader_speed with storage mgs:temp _escort

# A big pathfinding budget affords stair detours (PATHFINDING_RANGE); the command triggers the live budget recompute.
execute as @n[tag=mgs.zb_escort_new] run attribute @s minecraft:follow_range base set 96

# Monkey-bomb escorts target the thrown monkey: the flag routes retarget to retarget_monkey.
execute if score #zb_escort_mode mgs.data matches 1 run tag @n[tag=mgs.zb_escort_new] add mgs.zb_escort_monkey

# Walk-to spawns: the destination never moves, so the trader carries its own copy.
execute if score #zb_escort_mode mgs.data matches 2 run tag @n[tag=mgs.zb_escort_new] add mgs.zb_escort_walk
execute if score #zb_escort_mode mgs.data matches 2 run data modify entity @n[tag=mgs.zb_escort_new] data.walk_to set from entity @s data.walk_to
scoreboard players set #zb_escort_mode mgs.data 0

execute as @n[tag=mgs.zb_escort_new] at @s run function mgs:v5.1.0/zombies/escort/retarget

tag @n[tag=mgs.zb_escort_new] remove mgs.zb_escort_new
scoreboard players add #zb_escort_count mgs.data 1

