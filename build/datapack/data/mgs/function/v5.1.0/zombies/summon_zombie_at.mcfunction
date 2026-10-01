
#> mgs:v5.1.0/zombies/summon_zombie_at
#
# @executed	as @n[tag=mgs.zb_near,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/do_spawn_zombie with storage mgs:temp _zpos
#
# @args		type (unknown)
#			level (unknown)
#

# The marker passenger intercepts death before vanilla event 60 (poof particles).
# follow_range also sets the pathfinding region (range + 16) and node budget (range x 16); 40 keeps repaths cheap.
# step_height 1.0 makes 1-block rises walkable nodes instead of jump nodes that stall on stairs and slabs.
# zb_new names this zombie for the lines below: up to 20 rise at once from round 20, so @n[tag=zb_rising] can pick another.
summon minecraft:zombie ~ ~-2 ~ {Tags:["mgs.zombie_round","mgs.gm_entity","mgs.nukable","mgs.zb_rising","mgs.zb_new"],CanPickUpLoot:false,PersistenceRequired:true,DeathLootTable:"minecraft:empty",NoAI:1b,Silent:1b,Passengers:[{id:"minecraft:marker",Tags:["mgs.death_watch","mgs.gm_entity"]}],attributes:[{id:"minecraft:follow_range",base:40.0d},{id:"minecraft:step_height",base:1.0d}]}

$execute as @n[tag=mgs.zb_new] run function mgs:v5.1.0/zombies/types/$(type) {level:"$(level)"}

# Allied with escort traders, so traders do not flee the horde and zombies do not attack them (see escort).
team join mgs.horde @n[tag=mgs.zb_new]

execute as @n[tag=mgs.zb_new] run scoreboard players operation @s mgs.zb.stuck_ticks = #total_tick mgs.data
execute as @n[tag=mgs.zb_new] store result score @s mgs.zb.stuck_x run data get entity @s Pos[0]
execute as @n[tag=mgs.zb_new] store result score @s mgs.zb.stuck_z run data get entity @s Pos[2]
scoreboard players set @n[tag=mgs.zb_new] mgs.zb.stuck_dist 4

