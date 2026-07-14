
#> mgs:v5.1.0/zombies/powerups/check_drop
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/on_zombie_dying
#

# Only drop when a player's weapon killed this zombie (hit within the last 100 ticks),
# never from nukes/traps/environmental deaths. @s = the dying zombie.
scoreboard players operation #pu_hit_cutoff mgs.data = #total_tick mgs.data
scoreboard players remove #pu_hit_cutoff mgs.data 100
execute unless score @s mgs.zb.player_hit >= #pu_hit_cutoff mgs.data run return 0

# Stop once a full drop cycle (one shuffle-bag worth) has dropped this round
execute if score #zb_cycle_done mgs.data matches 1 run return 0

# Drop chance = min(2%, 2/total_round_zombies), expressed in basis points (per 10000).
# 2% = 200 bp; 1/total = 10000/total bp. Take the smaller of the two.
scoreboard players set #pu_chance_bp mgs.data 200
execute if score #zb_round_total mgs.data matches 1.. run scoreboard players set #pu_chance_tmp mgs.data 10000
execute if score #zb_round_total mgs.data matches 1.. run scoreboard players operation #pu_chance_tmp mgs.data /= #zb_round_total mgs.data
execute if score #zb_round_total mgs.data matches 1.. if score #pu_chance_tmp mgs.data < #pu_chance_bp mgs.data run scoreboard players operation #pu_chance_bp mgs.data = #pu_chance_tmp mgs.data

# Roll against the chance
execute store result score #pu_rng_roll mgs.data run random value 1..10000
execute unless score #pu_rng_roll mgs.data <= #pu_chance_bp mgs.data run return 0

# Passed: draw and spawn at this entity's position
function mgs:v5.1.0/zombies/powerups/spawn_random_at_self

# Count the drop; once a full cycle has dropped, no more drops this round
scoreboard players add #zb_drops_this_round mgs.data 1
execute if score #zb_drops_this_round mgs.data >= #zb_cycle_len mgs.data run scoreboard players set #zb_cycle_done mgs.data 1

