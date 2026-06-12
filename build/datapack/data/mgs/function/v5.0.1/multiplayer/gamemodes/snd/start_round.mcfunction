
#> mgs:v5.0.1/multiplayer/gamemodes/snd/start_round
#
# @within	mgs:v5.0.1/multiplayer/gamemodes/snd/setup
#			mgs:v5.0.1/multiplayer/gamemodes/snd/next_round 60t [ scheduled ]
#

# Guard: only while the game is running (a scheduled call may fire after the game ended)
execute if data storage mgs:multiplayer game{state:"lobby"} run return fail
execute if data storage mgs:multiplayer game{state:"ended"} run return fail

# Announce round
tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],[{"text":"────── ","color":"gold"}, {"translate":"mgs.round"}],{"score":{"name":"#snd_round","objective":"mgs.data"},"color":"yellow"},{"text":" ──────","color":"gold"}]

# Show which team attacks
execute if score #snd_attackers mgs.data matches 1 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.red","color":"red"},[{"text":" "}, {"translate":"mgs.attacks"}, " | "],{"translate":"mgs.blue","color":"blue"},[{"text":" "}, {"translate":"mgs.defends"}]]
execute if score #snd_attackers mgs.data matches 2 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"},[{"text":" "}, {"translate":"mgs.attacks"}, " | "],{"translate":"mgs.red","color":"red"},[{"text":" "}, {"translate":"mgs.defends"}]]
playsound minecraft:block.note_block.harp player @a ~ ~ ~ 1 1.0

# Reset bomb state and channel progress
scoreboard players set #snd_bomb_state mgs.data 0
scoreboard players set #snd_bomb_timer mgs.data 0
scoreboard players set #snd_plant_progress mgs.data 0
scoreboard players set #snd_defuse_progress mgs.data 0

# Reset round timer
scoreboard players set #snd_round_timer mgs.data 1800

# Restore players who died last round (S&D deaths skip the respawn countdown)
execute as @a[scores={mgs.mp.team=1..2},gamemode=spectator] run spectate @s
gamemode adventure @a[scores={mgs.mp.team=1..2},gamemode=spectator]

# Tag alive players
tag @a[scores={mgs.mp.team=1..2},gamemode=!spectator] add mgs.snd_alive

# Teleport everyone to their team spawns and re-apply class loadouts
execute as @a[scores={mgs.mp.team=1}] at @s run function mgs:v5.0.1/multiplayer/pick_spawn {type:"red"}
execute as @a[scores={mgs.mp.team=2}] at @s run function mgs:v5.0.1/multiplayer/pick_spawn {type:"blue"}
tag @e[tag=mgs.spawn_used] remove mgs.spawn_used
execute as @a[scores={mgs.mp.team=1..2}] at @s run function mgs:v5.0.1/multiplayer/apply_class

