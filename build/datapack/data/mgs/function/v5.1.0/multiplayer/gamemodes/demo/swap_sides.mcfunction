
#> mgs:v5.1.0/multiplayer/gamemodes/demo/swap_sides
#
# @executed	as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/next_round
#

execute if score #demo_attackers mgs.data matches 1 run scoreboard players set #demo_attackers mgs.data 2
execute unless score #demo_attackers mgs.data matches 2 run scoreboard players set #demo_attackers mgs.data 1
tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"⚔ ",{"translate":"mgs.sides_swapped","color":"gold"}]
playsound minecraft:block.note_block.xylophone player @a ~ ~ ~ 1 1.0

