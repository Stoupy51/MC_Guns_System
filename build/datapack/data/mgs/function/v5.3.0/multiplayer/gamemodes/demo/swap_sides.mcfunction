
#> mgs:v5.3.0/multiplayer/gamemodes/demo/swap_sides
#
# @executed	as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s
#
# @within	mgs:v5.3.0/multiplayer/gamemodes/demo/next_round
#

execute if score #demo_attackers mgs.data matches 1 run scoreboard players set #demo_attackers mgs.data 2
execute unless score #demo_attackers mgs.data matches 2 run scoreboard players set #demo_attackers mgs.data 1
tellraw @a[scores={mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"text":"⚔ ","color":"white"},{"translate":"mgs.sides_swapped","fallback":"Sides swapped!","color":"gold"}]
playsound minecraft:block.note_block.xylophone player @a[scores={mgs.mp.in_game=1}] ~ ~ ~ 1 1.0

