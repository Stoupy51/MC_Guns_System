
#> mgs:v5.0.0/multiplayer/stop
#
# @within	mgs:v5.0.0/multiplayer/team_wins
#

# End game
data modify storage mgs:multiplayer game.state set value "lobby"

# Signal game end
function #mgs:multiplayer/on_game_end

# Announce scores
tellraw @a ["",{"translate": "mgs.game_over","color":"gold","bold":true}]
tellraw @a ["",{"translate": "mgs.red","color":"red"},{"text":": "},{"score":{"name":"#red","objective":"mgs.mp.team"}}," | ",{"translate": "mgs.blue","color":"blue"},{"text":": "},{"score":{"name":"#blue","objective":"mgs.mp.team"}}]

# Clear teams
scoreboard players set @a mgs.mp.team 0

