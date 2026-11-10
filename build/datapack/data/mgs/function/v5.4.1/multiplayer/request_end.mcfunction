
#> mgs:v5.4.1/multiplayer/request_end
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/team_wins
#			mgs:v5.4.1/multiplayer/game_draw
#			mgs:v5.4.1/multiplayer/gamemodes/ffa/player_wins
#

scoreboard players operation #mp_end_tick mgs.data = #total_tick mgs.data

# Inside a kill, the death logged next is the final kill (see kill_cam/on_death).
execute if entity @a[tag=mgs.temp_victim] run scoreboard players set #kc_final mgs.data 1

