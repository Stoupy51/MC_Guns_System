
#> mgs:v5.1.0/multiplayer/gamemodes/snd/next_round
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/attackers_win
#			mgs:v5.1.0/multiplayer/gamemodes/snd/defenders_win
#

# The win function already cleared #snd_round_active, so the cleared snd_alive tags are not read as a wipe.
# The HUD clock resets here too: the tick does not drive it between rounds.
scoreboard players set #mp_timer mgs.data 3000
kill @e[tag=mgs.snd_bomb]
kill @e[tag=mgs.snd_bomb_vis]
kill @e[tag=mgs.snd_bomb_hud]
kill @e[tag=mgs.snd_loose]
kill @e[tag=mgs.snd_carrier_label]
tag @a remove mgs.snd_carrier
tag @a remove mgs.snd_alive

# Threshold set in setup, also read by the sidebar.
execute if score #red mgs.mp.team >= #snd_win_threshold mgs.data run return run function mgs:v5.1.0/multiplayer/team_wins {team:"Red"}
execute if score #blue mgs.mp.team >= #snd_win_threshold mgs.data run return run function mgs:v5.1.0/multiplayer/team_wins {team:"Blue"}

# Sides swap at halftime.
scoreboard players add #snd_round mgs.data 1
execute if score #snd_round mgs.data matches 4 if score #snd_attackers mgs.data matches 1 run scoreboard players set #snd_attackers mgs.data 2
execute if score #snd_round mgs.data matches 4 if score #snd_attackers mgs.data matches 2 run scoreboard players set #snd_attackers mgs.data 1
execute if score #snd_round mgs.data matches 4 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"text":"⚔ ","color":"white"},{"translate":"mgs.sides_swapped","color":"gold"}]
execute if score #snd_round mgs.data matches 4 run playsound minecraft:block.note_block.xylophone player @a ~ ~ ~ 1 1.0
# 3 s later.
schedule function mgs:v5.1.0/multiplayer/gamemodes/snd/start_round 60t

