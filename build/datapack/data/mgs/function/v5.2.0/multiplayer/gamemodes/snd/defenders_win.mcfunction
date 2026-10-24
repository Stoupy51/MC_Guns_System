
#> mgs:v5.2.0/multiplayer/gamemodes/snd/defenders_win
#
# @within	mgs:v5.2.0/multiplayer/gamemodes/snd/tick
#			mgs:v5.2.0/multiplayer/gamemodes/snd/bomb_defused
#

# Same single-shot guard: the defuse takes this path, and the wiped-looking alive tags would be judged again each tick.
execute unless score #snd_round_active mgs.data matches 1 run return fail
scoreboard players set #snd_round_active mgs.data 0

execute if score #snd_attackers mgs.data matches 1 run scoreboard players add #blue mgs.mp.team 1
execute if score #snd_attackers mgs.data matches 2 run scoreboard players add #red mgs.mp.team 1
execute if score #snd_attackers mgs.data matches 1 run tellraw @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.blue","fallback":"Blue","color":"blue"},[{"text":" ","color":"yellow"}, {"translate":"mgs.defenders_win_the_round","fallback":"(Defenders) win the round!"}],[" ",{"text":"+20 XP","color":"gold"}]]
execute if score #snd_attackers mgs.data matches 1 run tellraw @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.blue","fallback":"Blue","color":"blue"},[{"text":" ","color":"yellow"}, {"translate":"mgs.defenders_win_the_round","fallback":"(Defenders) win the round!"}],[" ",{"text":"+5 XP","color":"gray"}]]
execute if score #snd_attackers mgs.data matches 1 as @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] run function mgs:v5.2.0/progression/mp/award_round_win
execute if score #snd_attackers mgs.data matches 1 as @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] run function mgs:v5.2.0/progression/mp/award_round_loss
execute if score #snd_attackers mgs.data matches 2 run tellraw @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.red","fallback":"Red","color":"red"},[{"text":" ","color":"yellow"}, {"translate":"mgs.defenders_win_the_round","fallback":"(Defenders) win the round!"}],[" ",{"text":"+20 XP","color":"gold"}]]
execute if score #snd_attackers mgs.data matches 2 run tellraw @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.red","fallback":"Red","color":"red"},[{"text":" ","color":"yellow"}, {"translate":"mgs.defenders_win_the_round","fallback":"(Defenders) win the round!"}],[" ",{"text":"+5 XP","color":"gray"}]]
execute if score #snd_attackers mgs.data matches 2 as @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] run function mgs:v5.2.0/progression/mp/award_round_win
execute if score #snd_attackers mgs.data matches 2 as @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] run function mgs:v5.2.0/progression/mp/award_round_loss
playsound minecraft:entity.player.levelup player @a[scores={mgs.mp.in_game=1}] ~ ~ ~ 1 1.0

function mgs:v5.2.0/multiplayer/gamemodes/snd/next_round

