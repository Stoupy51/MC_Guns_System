
#> mgs:v5.1.0/multiplayer/gamemodes/snd/setup
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/start
#

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.search_destroy_carry_the_bomb_to_a_site_or_defend_both","color":"yellow"}]

# Store base coordinates for offset
function mgs:v5.1.0/shared/load_base_coordinates {mode:"multiplayer"}

# Round tracking. Round wins ARE the shared team score (#red / #blue on mp.team): the sidebar and the
# end-of-game "Final Score" line both read those, so keeping private win counters here meant S&D showed
# an empty sidebar all match and then announced a winner with "Red: 0 vs Blue: 0". multiplayer/start
# already zeroes both, so they are only read from here on.
scoreboard players set #snd_round mgs.data 1
scoreboard players set #snd_max_rounds mgs.data 6

# Bomb state: 0=loose or carried, 2=planted (bomb_timer = explosion countdown)
# Plant/defuse channel progress are tracked separately so the countdown is never clobbered
scoreboard players set #snd_bomb_state mgs.data 0
scoreboard players set #snd_bomb_timer mgs.data 0
scoreboard players set #snd_plant_progress mgs.data 0
scoreboard players set #snd_defuse_progress mgs.data 0

# Round gate. 0 means "no round in progress": between rounds nobody carries snd_alive, which makes the
# tick's "one whole side is dead" checks read as a wipe. See next_round.
scoreboard players set #snd_round_active mgs.data 0

# Round timer
scoreboard players set #snd_round_timer mgs.data 3000

# Summon objective markers (relative → absolute)
scoreboard players set #snd_site_idx mgs.data 0
data modify storage mgs:temp _snd_iter set from storage mgs:multiplayer game.map.search_and_destroy
execute if data storage mgs:temp _snd_iter[0] run function mgs:v5.1.0/multiplayer/gamemodes/snd/summon_obj

# Decide sides from the map geometry, now that both the sites and the spawns exist
# (multiplayer/start runs summon_spawns before dispatching this setup)
function mgs:v5.1.0/multiplayer/gamemodes/snd/pick_sides

# Start round
function mgs:v5.1.0/multiplayer/gamemodes/snd/start_round

