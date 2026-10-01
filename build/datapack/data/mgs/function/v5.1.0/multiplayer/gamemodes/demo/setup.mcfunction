
#> mgs:v5.1.0/multiplayer/gamemodes/demo/setup
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/start
#

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.demolition_destroy_both_bomb_sites_or_hold_them_until_time_runs_","color":"yellow"}]

function mgs:v5.1.0/shared/load_base_coordinates {mode:"multiplayer"}

# Round wins are the shared team score (#red, #blue on mp.team), which the sidebar and Final Score line read; multiplayer/start zeroes them.
scoreboard players set #demo_round mgs.data 1

# 0 between rounds, so the 3 s gap judges nothing.
scoreboard players set #demo_round_active mgs.data 0

# Claiming #mp_timer stops multiplayer/game_tick from counting it down or ending the match on it:
# this clock stops on a plant and grows on a destroy.
scoreboard players set #demo_timer mgs.data 3600
scoreboard players set #mp_mode_owns_timer mgs.data 1

# From the same map points as Search & Destroy.
scoreboard players set #demo_site_idx mgs.data 0
data modify storage mgs:temp _demo_iter set from storage mgs:multiplayer game.map.search_and_destroy
execute if data storage mgs:temp _demo_iter[0] run function mgs:v5.1.0/multiplayer/gamemodes/demo/summon_obj

# Sides depend on the map geometry; multiplayer/start summons the spawns before this setup.
function mgs:v5.1.0/multiplayer/gamemodes/demo/pick_sides

function mgs:v5.1.0/multiplayer/gamemodes/demo/start_round

