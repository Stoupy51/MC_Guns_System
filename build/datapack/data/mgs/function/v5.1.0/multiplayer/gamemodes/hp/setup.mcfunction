
#> mgs:v5.1.0/multiplayer/gamemodes/hp/setup
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/start
#

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.hardpoint_control_the_zone_to_score","color":"yellow"}]

function mgs:v5.1.0/shared/load_base_coordinates {mode:"multiplayer"}

data modify storage mgs:multiplayer game.hp_zones set from storage mgs:multiplayer game.map.hardpoint

# 60 s per zone.
scoreboard players set #hp_rotate_timer mgs.data 1200

# For the sidebar.
scoreboard players set #hp_rotate_sec mgs.data 60

# Label of the current zone (A to E).
scoreboard players set #hp_zone_idx mgs.data 0

# Score every second.
scoreboard players set #hp_score_timer mgs.data 20

# XP throttles: the hold counter, and the once-per-hill capture flag that load_zone clears.
scoreboard players set #hp_xp_hold mgs.data 5

function mgs:v5.1.0/multiplayer/gamemodes/hp/load_zone

