
#> mgs:v5.1.0/multiplayer/gamemodes/demo/setup
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/start
#

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.demolition_destroy_both_bomb_sites_or_hold_them_until_time_runs_","color":"yellow"}]

# Store base coordinates for offset
function mgs:v5.1.0/shared/load_base_coordinates {mode:"multiplayer"}

# Round wins ARE the shared team score (#red / #blue on mp.team), which is what the sidebar and the
# end-of-game "Final Score" line read. multiplayer/start already zeroes both.
scoreboard players set #demo_round mgs.data 1

# Round gate. 0 means "no round in progress", so the 3s gap between rounds judges nothing.
scoreboard players set #demo_round_active mgs.data 0

# Claiming #mp_timer stops multiplayer/game_tick from decrementing it or ending the match on it: this
# mode's clock stops on a plant and grows on a destroy, neither of which a match time limit can express.
scoreboard players set #demo_timer mgs.data 3600
scoreboard players set #mp_mode_owns_timer mgs.data 1

# Summon objective markers (relative → absolute), from the same map points Search & Destroy uses
scoreboard players set #demo_site_idx mgs.data 0
data modify storage mgs:temp _demo_iter set from storage mgs:multiplayer game.map.search_and_destroy
execute if data storage mgs:temp _demo_iter[0] run function mgs:v5.1.0/multiplayer/gamemodes/demo/summon_obj

# Decide sides from the map geometry, now that both the sites and the spawns exist
# (multiplayer/start runs summon_spawns before dispatching this setup)
function mgs:v5.1.0/multiplayer/gamemodes/demo/pick_sides

# Start round
function mgs:v5.1.0/multiplayer/gamemodes/demo/start_round

