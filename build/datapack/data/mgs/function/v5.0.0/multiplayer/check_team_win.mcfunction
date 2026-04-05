
#> mgs:v5.0.0/multiplayer/check_team_win
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/tdm/on_kill
#			mgs:v5.0.0/multiplayer/gamemodes/dom/score_tick
#			mgs:v5.0.0/multiplayer/gamemodes/hp/score_tick
#

execute store result score #score_limit mgs.data run data get storage mgs:multiplayer game.score_limit
execute if score #red mgs.mp.team >= #score_limit mgs.data run function mgs:v5.0.0/multiplayer/team_wins {team:"Red"}
execute if score #blue mgs.mp.team >= #score_limit mgs.data run function mgs:v5.0.0/multiplayer/team_wins {team:"Blue"}

