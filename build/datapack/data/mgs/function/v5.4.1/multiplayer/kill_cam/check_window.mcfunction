
#> mgs:v5.4.1/multiplayer/kill_cam/check_window
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/end_prep
#			mgs:v5.4.1/multiplayer/gamemodes/snd/start_round
#			mgs:v5.4.1/multiplayer/kill_cam/on_death
#

# The other modes end on points, sites or the clock.
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} unless data storage mgs:multiplayer game{gamemode:"tdm"} unless data storage mgs:multiplayer game{gamemode:"snd"} run return fail

# The lead: FFA's best player or the best team, against the score limit minus one full chain, or one round win short in S&D.
scoreboard players set #kc_lead mgs.data 0
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run scoreboard players operation #kc_lead mgs.data > @a[scores={mgs.mp.in_game=1}] mgs.mp.kills
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} run scoreboard players operation #kc_lead mgs.data > #red mgs.mp.team
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} run scoreboard players operation #kc_lead mgs.data > #blue mgs.mp.team

execute store result score #kc_threshold mgs.data run data get storage mgs:multiplayer game.score_limit
scoreboard players remove #kc_threshold mgs.data 6
execute if data storage mgs:multiplayer game{gamemode:"snd"} run scoreboard players operation #kc_threshold mgs.data = #snd_win_threshold mgs.data
execute if data storage mgs:multiplayer game{gamemode:"snd"} run scoreboard players remove #kc_threshold mgs.data 1

execute if score #kc_lead mgs.data >= #kc_threshold mgs.data run function mgs:v5.4.1/multiplayer/kill_cam/open

