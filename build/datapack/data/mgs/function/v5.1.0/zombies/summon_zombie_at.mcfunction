
#> mgs:v5.1.0/zombies/summon_zombie_at
#
# @executed	as @n[tag=mgs.zb_near,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/do_spawn_zombie with storage mgs:temp _zpos
#
# @args		type (unknown)
#			level (unknown)
#

# Summon zombie 2 blocks underground with NoAI (rise animation in progress)
# Attach a marker passenger so death can be intercepted before vanilla event 60 (poof particles).
# follow_range drives BOTH target acquisition AND the pathfinding region/node budget
# (region radius = follow_range+16, nodes = follow_range*16). A huge value (2048) made every
# repath build a multi-thousand-block region and explore 32k+ nodes, so paths failed and zombies
# froze. A sane value (40, just above vanilla's 35) keeps pathfinding cheap and reliable; long-range
# targeting is unnecessary because zombies spawn next to players and stuck ones are teleport-rescued.
# step_height 1.0 (vanilla mobs get 0.6) is what makes a zombie walk a 1-block rise instead of
# jumping it: WalkNodeEvaluator reads this attribute, so full blocks become plainly walkable nodes
# rather than jump nodes that stall on stairs, slabs and map geometry. Barricades are unaffected —
# they stop zombies by freezing movement_speed, not by collision (barricades/tick.py).
# zb_new is a scratch tag naming THIS zombie, mirroring zb_dog_new; do_spawn_zombie retires it.
# Every follow-up below used to select @n[tag=zb_rising], which is wrong from round 20 on: the timer
# bottoms out at 1 tick while a rise lasts 20, so up to 20 rising zombies exist at once and the one
# summoned 2 blocks under the marker is rarely the nearest. Missing the team join is what made escort
# traders read the horde as hostile and flee it at AvoidEntityGoal's 0.5 modifier instead of walking
# at WanderToPositionGoal's 0.35, i.e. 43% over the round's zombie speed.
summon minecraft:zombie ~ ~-2 ~ {Tags:["mgs.zombie_round","mgs.gm_entity","mgs.nukable","mgs.zb_rising","mgs.zb_new"],CanPickUpLoot:false,PersistenceRequired:true,DeathLootTable:"minecraft:empty",NoAI:1b,Silent:1b,Passengers:[{id:"minecraft:marker",Tags:["mgs.death_watch","mgs.gm_entity"]}],Attributes:[{id:"minecraft:follow_range",base:40.0d},{id:"minecraft:step_height",base:1.0d}]}

# Apply type-specific scaling (health, speed, rise timer)
$execute as @n[tag=mgs.zb_new] run function mgs:v5.1.0/zombies/types/$(type) {level:"$(level)"}

# Ally with escort traders (escort.py: forCombat targeting fails between allies, so the trader
# never flees the horde and zombies never attack the pathfinding taxi)
team join mgs.horde @n[tag=mgs.zb_new]

# Initialize stuck detection scores (timestamp + XZ snapshot + distance bucket at spawn)
execute as @n[tag=mgs.zb_new] run scoreboard players operation @s mgs.zb.stuck_ticks = #total_tick mgs.data
execute as @n[tag=mgs.zb_new] store result score @s mgs.zb.stuck_x run data get entity @s Pos[0]
execute as @n[tag=mgs.zb_new] store result score @s mgs.zb.stuck_z run data get entity @s Pos[2]
scoreboard players set @n[tag=mgs.zb_new] mgs.zb.stuck_dist 4

