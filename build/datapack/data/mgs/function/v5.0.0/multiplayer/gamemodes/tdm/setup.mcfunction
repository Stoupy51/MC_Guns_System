
#> mgs:v5.0.0/multiplayer/gamemodes/tdm/setup
#
# @within	mgs:v5.0.0/multiplayer/start
#

# Auto-assign players with no team so team scores can increment
execute as @a[scores={mgs.mp.in_game=1,mgs.mp.team=0}] run function mgs:v5.0.0/multiplayer/auto_assign_team

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.team_deathmatch_first_team_to_the_score_limit_wins","color":"yellow"}]

