
#> mgs:v5.0.0/multiplayer/team_wins
#
# @within	mgs:v5.0.0/multiplayer/on_kill_signal {team:"Red"}
#			mgs:v5.0.0/multiplayer/on_kill_signal {team:"Blue"}
#
# @args		team (string)
#

# Announce winner
$tellraw @a ["",{"text":"🏆 ","color":"gold"},{"text":"$(team) Team Wins!","color":"gold","bold":true}]
tellraw @a ["",{"translate": "mgs.final_score_red","color":"white"},{"score":{"name":"#red","objective":"mgs.mp.team"},"color":"red"},{"translate": "mgs.vs_blue","color":"gray"},{"score":{"name":"#blue","objective":"mgs.mp.team"},"color":"blue"}]

# End game
function mgs:multiplayer/stop

