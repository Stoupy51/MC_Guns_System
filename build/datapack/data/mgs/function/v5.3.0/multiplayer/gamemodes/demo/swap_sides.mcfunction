
#> mgs:v5.3.0/multiplayer/gamemodes/demo/swap_sides
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/multiplayer/gamemodes/demo/next_round
#

execute if score #demo_attackers mgs.data matches 1 run scoreboard players set #demo_attackers mgs.data 2
execute unless score #demo_attackers mgs.data matches 2 run scoreboard players set #demo_attackers mgs.data 1
tellraw @a[scores={mgs.mp.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"text":"⚔ ","color":"white"},{"translate":"mgs.sides_swapped","fallback":"Sides swapped!","color":"gold"}]
playsound minecraft:block.note_block.xylophone player @a[scores={mgs.mp.in_game=1}] ~ ~ ~ 1 1.0

