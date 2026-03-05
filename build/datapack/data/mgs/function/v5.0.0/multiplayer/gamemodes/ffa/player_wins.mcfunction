
#> mgs:v5.0.0/multiplayer/gamemodes/ffa/player_wins
#
# @executed	as @a[scores={mgs.mp.in_game=1}]
#
# @within	mgs:v5.0.0/multiplayer/ffa_time_up [ as @a[scores={mgs.mp.in_game=1}] ]
#			mgs:v5.0.0/multiplayer/gamemodes/ffa/tick [ as @a ]
#			mgs:v5.0.0/multiplayer/gamemodes/ffa/on_kill
#

# Announce winner using player's name
tellraw @a ["",{"text":"🏆 ","color":"gold"},{"selector":"@s","color":"gold","bold":true},{"translate": "mgs.wins","color":"gold","bold":true}]
tellraw @a ["",{"translate": "mgs.score","color":"gray"},{"score":{"name":"@s","objective":"mgs.mp.kills"},"color":"yellow"},{"translate": "mgs.kills","color":"gray"}]

# End game
function mgs:v5.0.0/multiplayer/stop

