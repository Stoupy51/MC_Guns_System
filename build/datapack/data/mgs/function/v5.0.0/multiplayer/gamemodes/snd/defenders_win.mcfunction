
#> mgs:v5.0.0/multiplayer/gamemodes/snd/defenders_win
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/snd/tick
#			mgs:v5.0.0/multiplayer/gamemodes/snd/bomb_defused
#

execute if score #snd_attackers mgs.data matches 1 run scoreboard players add #snd_blue_wins mgs.data 1
execute if score #snd_attackers mgs.data matches 1 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"},[{"text":" ","color":"yellow"}, {"translate":"mgs.defenders_win_the_round"}]]
execute if score #snd_attackers mgs.data matches 2 run scoreboard players add #snd_red_wins mgs.data 1
execute if score #snd_attackers mgs.data matches 2 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.red","color":"red"},[{"text":" ","color":"yellow"}, {"translate":"mgs.defenders_win_the_round"}]]
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1.0

function mgs:v5.0.0/multiplayer/gamemodes/snd/next_round

