
#> mgs:v5.0.0/multiplayer/gamemodes/snd/next_round
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/snd/attackers_win
#			mgs:v5.0.0/multiplayer/gamemodes/snd/defenders_win
#

# Clean round state
kill @e[tag=mgs.snd_bomb]
tag @a remove mgs.snd_alive

# Check if either team won enough rounds (best of max_rounds)
scoreboard players set #snd_win_threshold mgs.data 4
execute if score #snd_red_wins mgs.data >= #snd_win_threshold mgs.data run function mgs:v5.0.0/multiplayer/team_wins {team:"Red"}
execute if score #snd_blue_wins mgs.data >= #snd_win_threshold mgs.data run function mgs:v5.0.0/multiplayer/team_wins {team:"Blue"}

# Swap sides at halftime (after round 3)
scoreboard players add #snd_round mgs.data 1
execute if score #snd_round mgs.data matches 4 if score #snd_attackers mgs.data matches 1 run scoreboard players set #snd_attackers mgs.data 2
execute if score #snd_round mgs.data matches 4 if score #snd_attackers mgs.data matches 2 run scoreboard players set #snd_attackers mgs.data 1
execute if score #snd_round mgs.data matches 4 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.sides_swapped","color":"gold"}]
execute if score #snd_round mgs.data matches 4 run playsound minecraft:block.note_block.xylophone player @a ~ ~ ~ 1 1.0
# Start next round (delay 3 seconds = 60 ticks via schedule)
schedule function mgs:v5.0.0/multiplayer/gamemodes/snd/start_round 60t

