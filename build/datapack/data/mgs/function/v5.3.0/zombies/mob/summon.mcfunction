
#> mgs:v5.3.0/zombies/mob/summon
#
# @executed	positioned ~ ~-1.8 ~
#
# @within	mgs:v5.3.0/zombies/mob/spawn with storage mgs:temp _mob
#			mgs:v5.3.0/zombies/mob/rider with storage mgs:temp _mob
#
# @args		entity (unknown)
#			no_ai (unknown)
#

# The marker passenger intercepts death before vanilla event 60 (poof particles), 17 ticks after the death with DeathTime -16.
# follow_range also sets the pathfinding region (range + 16) and node budget (range x 16); 40 keeps repaths cheap.
# step_height 1.0 makes 1-block rises walkable nodes instead of jump nodes that stall on stairs and slabs.
$summon $(entity) ~ ~ ~ {Tags:["mgs.zb_new"],NoAI:$(no_ai),DeathTime:-16s,PersistenceRequired:true,CanPickUpLoot:false,DeathLootTable:"minecraft:empty",Passengers:[{id:"minecraft:marker",Tags:["mgs.death_watch","mgs.zombies_entity"],CustomName:"Death Watch"}],attributes:[{id:"minecraft:follow_range",base:40.0d},{id:"minecraft:step_height",base:1.0d}]}

