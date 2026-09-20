
#> mgs:v5.1.0/zombies/store_spawn_walk_to
#
# @within	mgs:v5.1.0/zombies/summon_spawn_iter
#

execute store result score #swx mgs.data run data get storage mgs:temp _spawn_iter[0].walk_to[0]
execute store result score #swy mgs.data run data get storage mgs:temp _spawn_iter[0].walk_to[1]
execute store result score #swz mgs.data run data get storage mgs:temp _spawn_iter[0].walk_to[2]
scoreboard players operation #swx mgs.data += #sx mgs.data
scoreboard players operation #swy mgs.data += #sy mgs.data
scoreboard players operation #swz mgs.data += #sz mgs.data
execute store result storage mgs:temp _walk_to.x int 1 run scoreboard players get #swx mgs.data
execute store result storage mgs:temp _walk_to.y int 1 run scoreboard players get #swy mgs.data
execute store result storage mgs:temp _walk_to.z int 1 run scoreboard players get #swz mgs.data
data modify entity @n[tag=mgs.new_spawn] data.walk_to set from storage mgs:temp _walk_to

