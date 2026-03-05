
#> mgs:v5.0.0/multiplayer/gamemodes/snd/start_round
#
# @within	mgs:v5.0.0/multiplayer/gamemodes/snd/setup
#			mgs:v5.0.0/multiplayer/gamemodes/snd/next_round 60t [ scheduled ]
#

# Announce round
tellraw @a [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.round","color":"gold"},{"score":{"name":"#snd_round","objective":"mgs.data"},"color":"yellow"},{"text":" ──────","color":"gold"}]

# Show which team attacks
execute if score #snd_attackers mgs.data matches 1 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.red","color":"red"},{"translate": "mgs.attacks"},{"translate": "mgs.blue","color":"blue"},{"translate": "mgs.defends"}]
execute if score #snd_attackers mgs.data matches 2 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.blue","color":"blue"},{"translate": "mgs.attacks"},{"translate": "mgs.red","color":"red"},{"translate": "mgs.defends"}]
playsound minecraft:block.note_block.harp player @a ~ ~ ~ 1 1.0

# Reset bomb state
scoreboard players set #snd_bomb_state mgs.data 0
scoreboard players set #snd_bomb_timer mgs.data 0

# Reset round timer
scoreboard players set #snd_round_timer mgs.data 1800

# Tag alive players
tag @a[scores={mgs.mp.team=1..2}] add mgs.snd_alive

# Respawn all players at team spawns
execute as @a[scores={mgs.mp.team=1..2}] at @s run function mgs:v5.0.0/multiplayer/apply_class

