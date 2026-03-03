
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
tellraw @a ["",{"text":"  Red: ","color":"red"},{"score":{"name":"#red","objective":"mgs.mp.team"},"color":"white"},{"text":" | Blue: ","color":"blue"},{"score":{"name":"#blue","objective":"mgs.mp.team"},"color":"white"}]

# Clear teams
scoreboard players set @a mgs.mp.team 0

