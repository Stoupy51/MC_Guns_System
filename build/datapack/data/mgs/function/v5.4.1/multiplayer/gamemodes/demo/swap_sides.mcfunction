
#> mgs:v5.4.1/multiplayer/gamemodes/demo/swap_sides
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/gamemodes/demo/next_round
#

# 1 becomes 2 and 2 becomes 1.
execute store result score #demo_attackers mgs.data if score #demo_attackers mgs.data matches 1
scoreboard players add #demo_attackers mgs.data 1
tellraw @a[scores={mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"text":"⚔ ","color":"white"},{"translate":"mgs.sides_swapped","fallback":"Sides swapped!","color":"gold"}]
playsound minecraft:block.note_block.xylophone player @a[scores={mgs.mp.in_game=1}] ~ ~ ~ 1 1.0

