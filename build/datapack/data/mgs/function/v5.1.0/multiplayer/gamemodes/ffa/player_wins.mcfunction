
#> mgs:v5.1.0/multiplayer/gamemodes/ffa/player_wins
#
# @executed	as @a[scores={mgs.mp.in_game=1}]
#
# @within	mgs:v5.1.0/multiplayer/ffa_time_up [ as @a[scores={mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/gamemodes/ffa/tick [ as @a ]
#			mgs:v5.1.0/multiplayer/gamemodes/ffa/on_kill
#

# FFA has no team score for multiplayer/xp/on_game_end to read, so the winner is marked here instead.
tag @s add mgs.xp_winner

# Announce winner using player's name
tellraw @a ["","🏆 ",["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.mp.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s","color":"gold","bold":true}]," ",{"translate":"mgs.wins","color":"gold","bold":true}]
tellraw @a ["","  ",{"translate":"mgs.score","color":"gray"},{"score":{"name":"@s","objective":"mgs.mp.kills"},"color":"yellow"}," ",{"translate":"mgs.kills","color":"gray"}]

# End game
function mgs:v5.1.0/multiplayer/stop

