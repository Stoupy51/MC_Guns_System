
#> mgs:v5.0.0/multiplayer/team_wins
#
# @within	mgs:v5.0.0/multiplayer/time_up {team:"Red"}
#			mgs:v5.0.0/multiplayer/time_up {team:"Blue"}
#			mgs:v5.0.0/multiplayer/gamemodes/tdm/on_kill {team:"Red"}
#			mgs:v5.0.0/multiplayer/gamemodes/tdm/on_kill {team:"Blue"}
#			mgs:v5.0.0/multiplayer/gamemodes/dom/score_tick {team:"Red"}
#			mgs:v5.0.0/multiplayer/gamemodes/dom/score_tick {team:"Blue"}
#			mgs:v5.0.0/multiplayer/gamemodes/hp/score_tick {team:"Red"}
#			mgs:v5.0.0/multiplayer/gamemodes/hp/score_tick {team:"Blue"}
#			mgs:v5.0.0/multiplayer/gamemodes/snd/next_round {team:"Red"}
#			mgs:v5.0.0/multiplayer/gamemodes/snd/next_round {team:"Blue"}
#
# @args		team (string)
#

# Announce winner
$tellraw @a ["",{"text":"🏆 ","color":"gold"},{"text":"$(team) Team Wins!","color":"gold","bold":true}]
tellraw @a ["",[{"text":"","color":"gray"},"  ",{"translate":"mgs.final_score_red"},": "],{"score":{"name":"#red","objective":"mgs.mp.team"},"color":"red"},[{"text":"","color":"gray"}," ",{"translate":"mgs.vs_blue"},": "],{"score":{"name":"#blue","objective":"mgs.mp.team"},"color":"blue"}]

# End game
function mgs:v5.0.0/multiplayer/stop

