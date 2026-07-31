
#> mgs:v5.1.0/multiplayer/gamemodes/snd/attackers_win
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/tick
#			mgs:v5.1.0/multiplayer/gamemodes/snd/bomb_explodes
#

# Close the round exactly once. Several end conditions can come true on the same tick (a defuse that
# also wipes a side, a timeout landing with the last kill), and each one calls in here.
execute unless score #snd_round_active mgs.data matches 1 run return fail
scoreboard players set #snd_round_active mgs.data 0

execute if score #snd_attackers mgs.data matches 1 run scoreboard players add #red mgs.mp.team 1
execute if score #snd_attackers mgs.data matches 2 run scoreboard players add #blue mgs.mp.team 1
execute if score #snd_attackers mgs.data matches 1 run tellraw @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.red","color":"red"},[{"text":" ","color":"yellow"}, {"translate":"mgs.attackers_win_the_round"}],[" ",{"text":"+20 XP","color":"gold"}]]
execute if score #snd_attackers mgs.data matches 1 run tellraw @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.red","color":"red"},[{"text":" ","color":"yellow"}, {"translate":"mgs.attackers_win_the_round"}],[" ",{"text":"+5 XP","color":"gray"}]]
execute if score #snd_attackers mgs.data matches 1 as @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] run function mgs:v5.1.0/progression/mp/award_round_win
execute if score #snd_attackers mgs.data matches 1 as @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] run function mgs:v5.1.0/progression/mp/award_round_loss
execute if score #snd_attackers mgs.data matches 2 run tellraw @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"},[{"text":" ","color":"yellow"}, {"translate":"mgs.attackers_win_the_round"}],[" ",{"text":"+20 XP","color":"gold"}]]
execute if score #snd_attackers mgs.data matches 2 run tellraw @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"},[{"text":" ","color":"yellow"}, {"translate":"mgs.attackers_win_the_round"}],[" ",{"text":"+5 XP","color":"gray"}]]
execute if score #snd_attackers mgs.data matches 2 as @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] run function mgs:v5.1.0/progression/mp/award_round_win
execute if score #snd_attackers mgs.data matches 2 as @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] run function mgs:v5.1.0/progression/mp/award_round_loss
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1.0

function mgs:v5.1.0/multiplayer/gamemodes/snd/next_round

