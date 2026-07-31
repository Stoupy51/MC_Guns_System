
#> mgs:v5.1.0/multiplayer/gamemodes/demo/attackers_win
#
# @executed	as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/site_destroyed
#

# Close the round exactly once: the last site's destruction and a clock expiry can land on the same tick
execute unless score #demo_round_active mgs.data matches 1 run return fail
scoreboard players set #demo_round_active mgs.data 0

execute if score #demo_attackers mgs.data matches 1 run scoreboard players add #red mgs.mp.team 1
execute if score #demo_attackers mgs.data matches 1 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.red","color":"red"},[{"text":" ","color":"yellow"}, {"translate":"mgs.destroyed_both_sites"}]]
execute if score #demo_attackers mgs.data matches 2 run scoreboard players add #blue mgs.mp.team 1
execute if score #demo_attackers mgs.data matches 2 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"},[{"text":" ","color":"yellow"}, {"translate":"mgs.destroyed_both_sites"}]]
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1.0

function mgs:v5.1.0/multiplayer/gamemodes/demo/next_round

