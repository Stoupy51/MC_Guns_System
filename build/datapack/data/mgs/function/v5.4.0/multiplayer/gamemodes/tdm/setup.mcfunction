
#> mgs:v5.4.0/multiplayer/gamemodes/tdm/setup
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/multiplayer/start
#

# Players with no team are assigned one, so team scores can rise.
execute as @a[scores={mgs.mp.in_game=1,mgs.mp.team=0}] run function mgs:v5.4.0/multiplayer/auto_assign_team

tellraw @a[scores={mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.team_deathmatch_first_team_to_the_score_limit_wins","fallback":"Team Deathmatch! First team to the score limit wins!","color":"yellow"}]

