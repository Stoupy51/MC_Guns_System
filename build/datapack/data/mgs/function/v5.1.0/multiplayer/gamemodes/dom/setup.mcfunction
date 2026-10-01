
#> mgs:v5.1.0/multiplayer/gamemodes/dom/setup
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/start
#

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.domination_capture_and_hold_zones_to_earn_points","color":"yellow"}]

function mgs:v5.1.0/shared/load_base_coordinates {mode:"multiplayer"}

# Labels A, B, C, ...
scoreboard players set #dom_zone_idx mgs.data 0

# Owner: 0 neutral, 1 red, 2 blue.
scoreboard players set #dom_owner_a mgs.data 0
scoreboard players set #dom_owner_b mgs.data 0
scoreboard players set #dom_owner_c mgs.data 0
scoreboard players set #dom_owner_d mgs.data 0
scoreboard players set #dom_owner_e mgs.data 0

scoreboard players set #dom_point_count mgs.data 0

data modify storage mgs:temp _dom_iter set from storage mgs:multiplayer game.map.domination
execute if data storage mgs:temp _dom_iter[0] run function mgs:v5.1.0/multiplayer/gamemodes/dom/summon_point

execute store result score #dom_point_count mgs.data if entity @e[tag=mgs.dom_point]

# Score every 5 s.
scoreboard players set #dom_score_timer mgs.data 100

