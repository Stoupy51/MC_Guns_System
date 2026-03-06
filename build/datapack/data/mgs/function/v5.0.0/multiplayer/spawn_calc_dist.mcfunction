
#> mgs:v5.0.0/multiplayer/spawn_calc_dist
#
# @executed	as @e[tag=mgs.spawn_candidate] & at @s
#
# @within	mgs:v5.0.0/multiplayer/pick_spawn [ as @e[tag=mgs.spawn_candidate] & at @s ]
#

# Get marker position
execute store result score #_mx mgs.data run data get entity @s Pos[0]
execute store result score #_my mgs.data run data get entity @s Pos[1]
execute store result score #_mz mgs.data run data get entity @s Pos[2]

# Get nearest enemy player position (expensive — caller limits candidates)
data modify storage mgs:temp _nearest set from entity @p[tag=mgs.spawn_enemy] Pos
execute store result score #_px mgs.data run data get storage mgs:temp _nearest[0]
execute store result score #_py mgs.data run data get storage mgs:temp _nearest[1]
execute store result score #_pz mgs.data run data get storage mgs:temp _nearest[2]

# dx, dy, dz
scoreboard players operation #_mx mgs.data -= #_px mgs.data
scoreboard players operation #_my mgs.data -= #_py mgs.data
scoreboard players operation #_mz mgs.data -= #_pz mgs.data

# distance = dx + dy + dz
scoreboard players operation #_mx mgs.data += #_my mgs.data
scoreboard players operation #_mx mgs.data += #_mz mgs.data

# Store on entity
scoreboard players operation @s mgs.data = #_mx mgs.data

