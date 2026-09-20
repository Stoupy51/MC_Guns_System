
#> mgs:v5.1.0/multiplayer/spawn_calc_dist
#
# @executed	as @e[tag=mgs.spawn_candidate] & at @s
#
# @within	mgs:v5.1.0/multiplayer/pick_spawn [ as @e[tag=mgs.spawn_candidate] & at @s ]
#

# Get marker position
execute store result score #mx mgs.data run data get entity @s Pos[0]
execute store result score #my mgs.data run data get entity @s Pos[1]
execute store result score #mz mgs.data run data get entity @s Pos[2]

# Get nearest enemy player position (the caller limits the candidate set)
execute at @p[tag=mgs.spawn_enemy] summon minecraft:marker run function mgs:v5.1.0/shared/probe_pos
execute store result score #px mgs.data run data get storage mgs:temp _probe_pos[0]
execute store result score #py mgs.data run data get storage mgs:temp _probe_pos[1]
execute store result score #pz mgs.data run data get storage mgs:temp _probe_pos[2]

# dx, dy, dz
scoreboard players operation #mx mgs.data -= #px mgs.data
scoreboard players operation #my mgs.data -= #py mgs.data
scoreboard players operation #mz mgs.data -= #pz mgs.data

# distance² = dx² + dy² + dz²
scoreboard players operation #mx mgs.data *= #mx mgs.data
scoreboard players operation #my mgs.data *= #my mgs.data
scoreboard players operation #mz mgs.data *= #mz mgs.data
scoreboard players operation #mx mgs.data += #my mgs.data
scoreboard players operation #mx mgs.data += #mz mgs.data

# Store on entity
scoreboard players operation @s mgs.data = #mx mgs.data

