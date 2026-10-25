
#> mgs:v5.3.0/multiplayer/gamemodes/ffa/player_wins
#
# @executed	as @a[scores={mgs.mp.in_game=1}]
#
# @within	mgs:v5.3.0/multiplayer/ffa_time_up [ as @a[scores={mgs.mp.in_game=1}] ]
#			mgs:v5.3.0/multiplayer/gamemodes/ffa/tick [ as @a ]
#			mgs:v5.3.0/multiplayer/gamemodes/ffa/on_kill
#

# FFA has no team score for multiplayer/xp/on_game_end, so the winner is marked here.
tag @s add mgs.xp_winner

tellraw @a[scores={mgs.mp.in_game=1}] ["","🏆 ",["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.mp.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s","color":"gold","bold":true}]," ",{"translate":"mgs.wins","fallback":"wins!","color":"gold","bold":true}]
tellraw @a[scores={mgs.mp.in_game=1}] ["","  ",{"translate":"mgs.score","fallback":"Score: ","color":"gray"},{"score":{"name":"@s","objective":"mgs.mp.kills"},"color":"yellow"}," ",{"translate":"mgs.kills","fallback":"kills","color":"gray"}]

function mgs:v5.3.0/multiplayer/stop

