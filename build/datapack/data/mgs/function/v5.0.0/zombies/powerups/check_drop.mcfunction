
#> mgs:v5.0.0/zombies/powerups/check_drop
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/on_zombie_dying
#

# Compute combined score of all in-game players
scoreboard players set #zb_total_score mgs.data 0
execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] run scoreboard players operation #zb_total_score mgs.data += @s mgs.zb.points

# Guard: max 4 drops per round
execute if score #zb_drops_this_round mgs.data matches 4.. run return 0

# Guard: combined score must meet threshold
execute unless score #zb_total_score mgs.data >= #zb_score_to_drop mgs.data run return 0

# Guard: 2% RNG check
execute store result score #pu_rng_roll mgs.data run random value 1..100
execute unless score #pu_rng_roll mgs.data matches 1..20 run return 0

# All checks passed: draw next type from the shuffle bag (no repeats until all 9 used)
function mgs:v5.0.0/zombies/powerups/queue_draw

# Spawn visuals at the pre-stored zombie death position
data modify storage mgs:temp _pu_spawn set value {x:0,y:0,z:0}
data modify storage mgs:temp _pu_spawn.x set from entity @s Pos[0]
data modify storage mgs:temp _pu_spawn.y set from entity @s Pos[1]
data modify storage mgs:temp _pu_spawn.z set from entity @s Pos[2]
function mgs:v5.0.0/zombies/powerups/do_spawn_random with storage mgs:temp _pu_spawn

# Multiply threshold by 1.14 so each subsequent drop requires more score
scoreboard players operation #zb_score_to_drop mgs.data *= #114 mgs.data
scoreboard players operation #zb_score_to_drop mgs.data /= #100 mgs.data

# Increment this round's drop counter
scoreboard players add #zb_drops_this_round mgs.data 1

