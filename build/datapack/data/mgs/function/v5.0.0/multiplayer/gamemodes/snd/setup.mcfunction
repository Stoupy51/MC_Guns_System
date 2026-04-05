
#> mgs:v5.0.0/multiplayer/gamemodes/snd/setup
#
# @within	mgs:v5.0.0/multiplayer/start
#

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.search_destroy_attackers_plant_defenders_defuse","color":"yellow"}]

# Store base coordinates for offset
function mgs:v5.0.0/shared/load_base_coordinates {mode:"multiplayer"}

# Round tracking
scoreboard players set #snd_round mgs.data 1
scoreboard players set #snd_max_rounds mgs.data 6
scoreboard players set #snd_red_wins mgs.data 0
scoreboard players set #snd_blue_wins mgs.data 0

# Red starts as attackers
scoreboard players set #snd_attackers mgs.data 1

# Bomb state: 0=not planted, 1=planting, 2=planted, 3=defusing
scoreboard players set #snd_bomb_state mgs.data 0
scoreboard players set #snd_bomb_timer mgs.data 0

# Round timer (90 seconds = 1800 ticks)
scoreboard players set #snd_round_timer mgs.data 1800

# Summon objective markers (relative → absolute)
data modify storage mgs:temp _snd_iter set from storage mgs:multiplayer game.map.search_and_destroy
execute if data storage mgs:temp _snd_iter[0] run function mgs:v5.0.0/multiplayer/gamemodes/snd/summon_obj

# Start round
function mgs:v5.0.0/multiplayer/gamemodes/snd/start_round

