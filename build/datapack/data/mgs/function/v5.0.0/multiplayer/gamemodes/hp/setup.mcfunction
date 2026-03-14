
#> mgs:v5.0.0/multiplayer/gamemodes/hp/setup
#
# @within	mgs:v5.0.0/multiplayer/start
#

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.hardpoint_control_the_zone_to_score","color":"yellow"}]

# Store base coordinates for offset
execute store result score #gm_base_x mgs.data run data get storage mgs:multiplayer game.map.base_coordinates[0]
execute store result score #gm_base_y mgs.data run data get storage mgs:multiplayer game.map.base_coordinates[1]
execute store result score #gm_base_z mgs.data run data get storage mgs:multiplayer game.map.base_coordinates[2]

# Copy hardpoint zones from map to game state
data modify storage mgs:multiplayer game.hp_zones set from storage mgs:multiplayer game.map.hardpoint

# Rotation timer (60 seconds = 1200 ticks per zone)
scoreboard players set #hp_rotate_timer mgs.data 1200

# Rotation timer in seconds for sidebar display
scoreboard players set #hp_rotate_sec mgs.data 60

# Scoring timer (score every 1 second = 20 ticks)
scoreboard players set #hp_score_timer mgs.data 20

# Load first zone
function mgs:v5.0.0/multiplayer/gamemodes/hp/load_zone

