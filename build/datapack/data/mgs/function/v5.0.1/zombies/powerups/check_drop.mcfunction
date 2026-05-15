
#> mgs:v5.0.1/zombies/powerups/check_drop
#
# @executed	at @s
#
# @within	mgs:v5.0.1/zombies/on_zombie_dying
#

# Compute combined score of all in-game players
scoreboard players set #zb_total_score mgs.data 0
execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] run scoreboard players operation #zb_total_score mgs.data += @s mgs.zb.points

# Guard: max 4 drops per round
execute if score #zb_drops_this_round mgs.data matches 4.. run return 0

# Guard: combined score must meet threshold
execute unless score #zb_total_score mgs.data >= #zb_score_to_drop mgs.data run return 0

# Guard: 4% RNG check
execute store result score #pu_rng_roll mgs.data run random value 1..100
execute unless score #pu_rng_roll mgs.data matches 1..4 run return 0

# All checks passed: draw and spawn at this entity's position
function mgs:v5.0.1/zombies/powerups/spawn_random_at_self

# Multiply threshold by 1.14 so each subsequent drop requires more score
scoreboard players operation #zb_score_to_drop mgs.data *= #114 mgs.data
scoreboard players operation #zb_score_to_drop mgs.data /= #100 mgs.data

# Increment this round's drop counter
scoreboard players add #zb_drops_this_round mgs.data 1

