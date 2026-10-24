
#> mgs:v5.2.0/multiplayer/gamemodes/demo/attackers_win
#
# @executed	as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s
#
# @within	mgs:v5.2.0/multiplayer/gamemodes/demo/site_destroyed
#

# Closes the round once: the last destruction and a clock expiry can land on the same tick.
execute unless score #demo_round_active mgs.data matches 1 run return fail
scoreboard players set #demo_round_active mgs.data 0

execute if score #demo_attackers mgs.data matches 1 run scoreboard players add #red mgs.mp.team 1
execute if score #demo_attackers mgs.data matches 2 run scoreboard players add #blue mgs.mp.team 1
execute if score #demo_attackers mgs.data matches 1 run tellraw @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.red","fallback":"Red","color":"red"},[{"text":" ","color":"yellow"}, {"translate":"mgs.destroyed_both_sites","fallback":"destroyed both sites!"}],[" ",{"text":"+20 XP","color":"gold"}]]
execute if score #demo_attackers mgs.data matches 1 run tellraw @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.red","fallback":"Red","color":"red"},[{"text":" ","color":"yellow"}, {"translate":"mgs.destroyed_both_sites","fallback":"destroyed both sites!"}],[" ",{"text":"+5 XP","color":"gray"}]]
execute if score #demo_attackers mgs.data matches 1 as @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] run function mgs:v5.2.0/progression/mp/award_round_win
execute if score #demo_attackers mgs.data matches 1 as @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] run function mgs:v5.2.0/progression/mp/award_round_loss
execute if score #demo_attackers mgs.data matches 2 run tellraw @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.blue","fallback":"Blue","color":"blue"},[{"text":" ","color":"yellow"}, {"translate":"mgs.destroyed_both_sites","fallback":"destroyed both sites!"}],[" ",{"text":"+20 XP","color":"gold"}]]
execute if score #demo_attackers mgs.data matches 2 run tellraw @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.blue","fallback":"Blue","color":"blue"},[{"text":" ","color":"yellow"}, {"translate":"mgs.destroyed_both_sites","fallback":"destroyed both sites!"}],[" ",{"text":"+5 XP","color":"gray"}]]
execute if score #demo_attackers mgs.data matches 2 as @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] run function mgs:v5.2.0/progression/mp/award_round_win
execute if score #demo_attackers mgs.data matches 2 as @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] run function mgs:v5.2.0/progression/mp/award_round_loss
playsound minecraft:entity.player.levelup player @a[scores={mgs.mp.in_game=1}] ~ ~ ~ 1 1.0

function mgs:v5.2.0/multiplayer/gamemodes/demo/next_round

