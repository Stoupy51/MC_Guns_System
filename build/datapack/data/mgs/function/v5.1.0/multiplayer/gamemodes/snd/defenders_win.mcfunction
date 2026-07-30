
#> mgs:v5.1.0/multiplayer/gamemodes/snd/defenders_win
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/tick
#			mgs:v5.1.0/multiplayer/gamemodes/snd/bomb_defused
#

# Same single-shot guard as attackers_win — this is the path the defuse takes, and the defuse used to be
# immediately followed by four attacker wins as the wiped-looking alive tags were judged tick after tick.
execute unless score #snd_round_active mgs.data matches 1 run return fail
scoreboard players set #snd_round_active mgs.data 0

execute if score #snd_attackers mgs.data matches 1 run scoreboard players add #blue mgs.mp.team 1
execute if score #snd_attackers mgs.data matches 1 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"},[{"text":" ","color":"yellow"}, {"translate":"mgs.defenders_win_the_round"}]]
execute if score #snd_attackers mgs.data matches 2 run scoreboard players add #red mgs.mp.team 1
execute if score #snd_attackers mgs.data matches 2 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.red","color":"red"},[{"text":" ","color":"yellow"}, {"translate":"mgs.defenders_win_the_round"}]]
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1.0

function mgs:v5.1.0/multiplayer/gamemodes/snd/next_round

