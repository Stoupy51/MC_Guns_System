
#> mgs:v5.2.0/multiplayer/team_wins
#
# @within	mgs:v5.2.0/multiplayer/check_team_win {team:"Red"}
#			mgs:v5.2.0/multiplayer/check_team_win {team:"Blue"}
#			mgs:v5.2.0/multiplayer/time_up {team:"Red"}
#			mgs:v5.2.0/multiplayer/time_up {team:"Blue"}
#			mgs:v5.2.0/multiplayer/gamemodes/snd/next_round {team:"Red"}
#			mgs:v5.2.0/multiplayer/gamemodes/snd/next_round {team:"Blue"}
#			mgs:v5.2.0/multiplayer/gamemodes/demo/next_round {team:"Red"}
#			mgs:v5.2.0/multiplayer/gamemodes/demo/next_round {team:"Blue"}
#
# @args		team (string)
#

$tellraw @a[scores={mgs.mp.in_game=1}] ["","🏆 ",{"text":"$(team) Team Wins!","color":"gold","bold":true}]
tellraw @a[scores={mgs.mp.in_game=1}] ["",[{"text":"","color":"gray"},"  ",{"translate":"mgs.final_score_red","fallback":"Final Score - Red"},": "],{"score":{"name":"#red","objective":"mgs.mp.team"},"color":"red"},[{"text":"","color":"gray"}," ",{"translate":"mgs.vs_blue","fallback":"vs Blue"},": "],{"score":{"name":"#blue","objective":"mgs.mp.team"},"color":"blue"}]

function mgs:v5.2.0/multiplayer/stop

