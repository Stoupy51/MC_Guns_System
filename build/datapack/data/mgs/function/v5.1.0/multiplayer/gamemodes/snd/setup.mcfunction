
#> mgs:v5.1.0/multiplayer/gamemodes/snd/setup
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/start
#

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.search_destroy_carry_the_bomb_to_a_site_or_defend_both","color":"yellow"}]

function mgs:v5.1.0/shared/load_base_coordinates {mode:"multiplayer"}

# Round wins are the shared team score (#red, #blue on mp.team), which the sidebar and the Final Score line read.
# multiplayer/start already zeroes them.
scoreboard players set #snd_round mgs.data 1
scoreboard players set #snd_win_threshold mgs.data 4

# 0 loose or carried, 2 planted (bomb_timer is the fuse); plant and defuse progress are separate, so the fuse is never overwritten.
scoreboard players set #snd_bomb_state mgs.data 0
scoreboard players set #snd_bomb_timer mgs.data 0
scoreboard players set #snd_plant_progress mgs.data 0
scoreboard players set #snd_defuse_progress mgs.data 0

# 0 between rounds, when nobody carries snd_alive and the wipe checks would fire (see next_round).
scoreboard players set #snd_round_active mgs.data 0

# The round timer also drives the HUD clock: claiming #mp_timer stops multiplayer/game_tick from counting it down and ending the match on it,
# since a 10-minute match limit cannot judge up to seven 2:30 rounds. start_round seeds the display.
scoreboard players set #snd_round_timer mgs.data 3000
scoreboard players set #mp_mode_owns_timer mgs.data 1

scoreboard players set #snd_site_idx mgs.data 0
data modify storage mgs:temp _snd_iter set from storage mgs:multiplayer game.map.search_and_destroy
execute if data storage mgs:temp _snd_iter[0] run function mgs:v5.1.0/multiplayer/gamemodes/snd/summon_obj

# Sides depend on the map geometry; multiplayer/start summons the spawns before this setup.
function mgs:v5.1.0/multiplayer/gamemodes/snd/pick_sides

function mgs:v5.1.0/multiplayer/gamemodes/snd/start_round

