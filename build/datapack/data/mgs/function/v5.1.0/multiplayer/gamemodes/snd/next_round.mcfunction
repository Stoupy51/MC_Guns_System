
#> mgs:v5.1.0/multiplayer/gamemodes/snd/next_round
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/attackers_win
#			mgs:v5.1.0/multiplayer/gamemodes/snd/defenders_win
#

# Clean round state. #snd_round_active was already cleared by the win function that got us here, which is
# what stops the tick from judging the cleared snd_alive tags below as a wipe.
# The HUD clock is reset here and not only in start_round: the tick stops driving it while no round is
# running, so the 3s gap would otherwise sit on the expired timer or the leftover fuse.
scoreboard players set #mp_timer mgs.data 3000
kill @e[tag=mgs.snd_bomb]
kill @e[tag=mgs.snd_bomb_vis]
kill @e[tag=mgs.snd_bomb_hud]
kill @e[tag=mgs.snd_loose]
kill @e[tag=mgs.snd_carrier_label]
tag @a remove mgs.snd_carrier
tag @a remove mgs.snd_alive

# Check if either team won enough rounds (best of max_rounds) — stop here on game win
scoreboard players set #snd_win_threshold mgs.data 4
execute if score #red mgs.mp.team >= #snd_win_threshold mgs.data run return run function mgs:v5.1.0/multiplayer/team_wins {team:"Red"}
execute if score #blue mgs.mp.team >= #snd_win_threshold mgs.data run return run function mgs:v5.1.0/multiplayer/team_wins {team:"Blue"}

# Swap sides at halftime
scoreboard players add #snd_round mgs.data 1
execute if score #snd_round mgs.data matches 4 if score #snd_attackers mgs.data matches 1 run scoreboard players set #snd_attackers mgs.data 2
execute if score #snd_round mgs.data matches 4 if score #snd_attackers mgs.data matches 2 run scoreboard players set #snd_attackers mgs.data 1
execute if score #snd_round mgs.data matches 4 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"⚔ ",{"translate":"mgs.sides_swapped","color":"gold"}]
execute if score #snd_round mgs.data matches 4 run playsound minecraft:block.note_block.xylophone player @a ~ ~ ~ 1 1.0
# Start next round (delay 3 seconds = 60 ticks via schedule)
schedule function mgs:v5.1.0/multiplayer/gamemodes/snd/start_round 60t

