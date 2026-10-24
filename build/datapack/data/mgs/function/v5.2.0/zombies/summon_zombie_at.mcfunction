
#> mgs:v5.2.0/zombies/summon_zombie_at
#
# @executed	as @n[tag=mgs.zb_near,sort=random] & at @s
#
# @within	mgs:v5.2.0/zombies/do_spawn_zombie with storage mgs:temp _zpos
#			mgs:v5.2.0/zombies/do_spawn_zombie with storage mgs:temp _zpos [ positioned ~ ~4 ~ ]
#
# @args		type (unknown)
#			level (unknown)
#

# The marker passenger intercepts death before vanilla event 60 (poof particles).
# follow_range also sets the pathfinding region (range + 16) and node budget (range x 16); 40 keeps repaths cheap.
# step_height 1.0 makes 1-block rises walkable nodes instead of jump nodes that stall on stairs and slabs.
# zb_new names this zombie for the lines below: up to 20 rise at once from round 20, so @n[tag=zb_rising] can pick another.
summon minecraft:zombie ~ ~-1.8 ~ {Tags:["mgs.zombie_round","mgs.zombies_entity","mgs.nukable","mgs.zb_rising","mgs.zb_new"],CanPickUpLoot:false,PersistenceRequired:true,DeathLootTable:"minecraft:empty",NoAI:1b,Silent:1b,Passengers:[{id:"minecraft:marker",Tags:["mgs.death_watch","mgs.zombies_entity"]}],attributes:[{id:"minecraft:follow_range",base:40.0d},{id:"minecraft:step_height",base:1.0d}]}

$execute as @n[tag=mgs.zb_new] run function mgs:v5.2.0/zombies/types/$(type) {level:"$(level)"}

# Allied with escort traders, so traders do not flee the horde and zombies do not attack them (see escort).
team join mgs.horde @n[tag=mgs.zb_new]

# Shown on the players' locator bar.
attribute @n[tag=mgs.zb_new] minecraft:waypoint_transmit_range base set 256
waypoint modify @n[tag=mgs.zb_new] color green

execute as @n[tag=mgs.zb_new] store result score @s mgs.zb.stuck_x run data get entity @s Pos[0]
execute as @n[tag=mgs.zb_new] store result score @s mgs.zb.stuck_z run data get entity @s Pos[2]
scoreboard players set @n[tag=mgs.zb_new] mgs.zb.stuck_dist 4

