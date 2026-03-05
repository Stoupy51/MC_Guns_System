
#> mgs:v5.0.0/multiplayer/gamemodes/snd/attackers_win
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/snd/tick
#			mgs:v5.0.0/multiplayer/gamemodes/snd/bomb_explodes
#

execute if score #snd_attackers mgs.data matches 1 run scoreboard players add #snd_red_wins mgs.data 1
execute if score #snd_attackers mgs.data matches 1 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.red","color":"red"},{"translate": "mgs.attackers_win_the_round","color":"yellow"}]
execute if score #snd_attackers mgs.data matches 2 run scoreboard players add #snd_blue_wins mgs.data 1
execute if score #snd_attackers mgs.data matches 2 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.blue","color":"blue"},{"translate": "mgs.attackers_win_the_round","color":"yellow"}]

function mgs:v5.0.0/multiplayer/gamemodes/snd/next_round

