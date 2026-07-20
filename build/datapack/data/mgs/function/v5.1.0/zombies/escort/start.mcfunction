
#> mgs:v5.1.0/zombies/escort/start
#
# @executed	as @e[tag=...,limit=24,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/on_stuck_zombie
#			mgs:v5.1.0/zombies/escort/update_lure [ as @e[tag=...,limit=2,sort=random] & at @s ]
#			mgs:v5.1.0/zombies/monkey/pull_one
#

# Freeze the zombie: the trader does the walking from here, the zombie is dragged behind it.
# The team join is normally redundant (round.py joins every zombie at summon) but covers
# zombies summoned before a mid-game /reload introduced the team.
tag @s add mgs.zb_escorted
team join mgs.horde @s
data modify entity @s NoAI set value 1b
scoreboard players set @s mgs.zb.escort_ttl 900

# Watchdog init: stuck_x/z/ticks are repurposed while escorted (block snapshot + still counter);
# detach re-initializes them for the normal stuck detection
execute store result score @s mgs.zb.stuck_x run data get entity @s Pos[0]
execute store result score @s mgs.zb.stuck_z run data get entity @s Pos[2]
scoreboard players set @s mgs.zb.stuck_ticks 0

# Invisible pathfinding taxi (see escort.py header for every NBT choice)
summon minecraft:wandering_trader ~ ~ ~ {Tags:["mgs.zb_escort","mgs.gm_entity","mgs.zb_escort_new","global.ignore","global.ignore.kill"],Silent:1b,Invulnerable:1b,PersistenceRequired:1b,DespawnDelay:0,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",Offers:{Recipes:[]},active_effects:[{id:"minecraft:invisibility",duration:-1,show_particles:0b}]}

# Allied with the horde so its AvoidEntityGoal(Zombie) never fires and zombies never target it
team join mgs.horde @n[tag=mgs.zb_escort_new]

# Trader base speed = zombie_speed / 0.35 (WanderToPositionGoal modifier) => same effective speed
execute store result storage mgs:temp _escort.speed double 0.0028571 run attribute @s minecraft:movement_speed get 1000
execute as @n[tag=mgs.zb_escort_new] run function mgs:v5.1.0/zombies/escort/set_trader_speed with storage mgs:temp _escort

# Big pathfinding budget so it can afford stair detours instead of camping below the player
# (see PATHFINDING_RANGE in escort.py; the command triggers the live budget recompute)
execute as @n[tag=mgs.zb_escort_new] run attribute @s minecraft:follow_range base set 96

# Monkey-bomb escorts (monkey_bomb.py) target the thrown monkey instead of a player: flag the
# trader so retarget routes to retarget_monkey. #zb_escort_mode is the caller's one-shot signal.
execute if score #zb_escort_mode mgs.data matches 1 run tag @n[tag=mgs.zb_escort_new] add mgs.zb_escort_monkey
scoreboard players set #zb_escort_mode mgs.data 0

# Aim it at its target immediately (nearest player, PaP-room lure, or thrown monkey per the flag)
execute as @n[tag=mgs.zb_escort_new] at @s run function mgs:v5.1.0/zombies/escort/retarget

tag @n[tag=mgs.zb_escort_new] remove mgs.zb_escort_new
scoreboard players add #zb_escort_count mgs.data 1

