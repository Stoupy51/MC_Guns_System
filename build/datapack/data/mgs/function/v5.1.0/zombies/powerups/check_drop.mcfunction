
#> mgs:v5.1.0/zombies/powerups/check_drop
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/on_zombie_dying
#

# Only when a player's weapon hit it within 100 ticks: never from nukes, traps or the environment.
scoreboard players operation #pu_hit_cutoff mgs.data = #total_tick mgs.data
scoreboard players remove #pu_hit_cutoff mgs.data 100
execute unless score @s mgs.zb.player_hit >= #pu_hit_cutoff mgs.data run return 0

# One shuffle bag per round at most.
execute if score #zb_cycle_done mgs.data matches 1 run return 0

# min(2%, 1 / round total) in basis points: 200 against 10000 / total.
scoreboard players set #pu_chance_bp mgs.data 200
execute if score #zb_round_total mgs.data matches 1.. run scoreboard players set #pu_chance_tmp mgs.data 10000
execute if score #zb_round_total mgs.data matches 1.. run scoreboard players operation #pu_chance_tmp mgs.data /= #zb_round_total mgs.data
execute if score #zb_round_total mgs.data matches 1.. if score #pu_chance_tmp mgs.data < #pu_chance_bp mgs.data run scoreboard players operation #pu_chance_bp mgs.data = #pu_chance_tmp mgs.data

execute store result score #pu_rng_roll mgs.data run random value 1..10000
execute unless score #pu_rng_roll mgs.data <= #pu_chance_bp mgs.data run return 0

function mgs:v5.1.0/zombies/powerups/spawn_random_at_self

scoreboard players add #zb_drops_this_round mgs.data 1
execute if score #zb_drops_this_round mgs.data >= #zb_cycle_len mgs.data run scoreboard players set #zb_cycle_done mgs.data 1

