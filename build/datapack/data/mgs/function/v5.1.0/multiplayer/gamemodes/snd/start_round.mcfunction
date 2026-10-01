
#> mgs:v5.1.0/multiplayer/gamemodes/snd/start_round
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/setup
#			mgs:v5.1.0/multiplayer/gamemodes/snd/next_round 60t [ scheduled ]
#

# A scheduled call may fire after the game ended.
execute if data storage mgs:multiplayer game{state:"lobby"} run return fail
execute if data storage mgs:multiplayer game{state:"ended"} run return fail

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],[{"text":"────── ","color":"gold"}, {"translate":"mgs.round_2"}],{"score":{"name":"#snd_round","objective":"mgs.data"},"color":"yellow"},{"text":" ──────","color":"gold"}]

execute if score #snd_attackers mgs.data matches 1 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.red","color":"red"},[{"text":" "}, {"translate":"mgs.attacks"}, " | "],{"translate":"mgs.blue","color":"blue"},[{"text":" "}, {"translate":"mgs.defends_2"}]]
execute if score #snd_attackers mgs.data matches 2 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"},[{"text":" "}, {"translate":"mgs.attacks"}, " | "],{"translate":"mgs.red","color":"red"},[{"text":" "}, {"translate":"mgs.defends_2"}]]
playsound minecraft:block.note_block.harp player @a ~ ~ ~ 1 1.0

scoreboard players set #snd_bomb_state mgs.data 0
scoreboard players set #snd_bomb_timer mgs.data 0
scoreboard players set #snd_plant_progress mgs.data 0
scoreboard players set #snd_defuse_progress mgs.data 0

# The HUD clock too, so the 3 s gap already shows 2:30.
scoreboard players set #snd_round_timer mgs.data 3000
scoreboard players set #mp_timer mgs.data 3000

# S&D deaths skip the respawn countdown.
execute as @a[scores={mgs.mp.team=1..2},gamemode=spectator] run spectate @s
gamemode adventure @a[scores={mgs.mp.team=1..2},gamemode=spectator]

tag @a[scores={mgs.mp.team=1..2},gamemode=!spectator] add mgs.snd_alive

execute as @a[scores={mgs.mp.team=1}] at @s run function mgs:v5.1.0/multiplayer/pick_spawn {type:"red"}
execute as @a[scores={mgs.mp.team=2}] at @s run function mgs:v5.1.0/multiplayer/pick_spawn {type:"blue"}
tag @e[tag=mgs.spawn_used] remove mgs.spawn_used
execute as @a[scores={mgs.mp.team=1..2}] at @s run function mgs:v5.1.0/multiplayer/apply_class

# One bomb per round, held by nobody: collecting it gives the defenders time to set up, unlike a Counter-Strike round.
tag @a remove mgs.snd_carrier
kill @e[tag=mgs.snd_loose]
kill @e[tag=mgs.snd_carrier_label]
execute if score #snd_attackers mgs.data matches 1 at @e[tag=mgs.spawn_red,limit=1] run function mgs:v5.1.0/multiplayer/gamemodes/snd/spawn_loose_bomb
execute if score #snd_attackers mgs.data matches 2 at @e[tag=mgs.spawn_blue,limit=1] run function mgs:v5.1.0/multiplayer/gamemodes/snd/spawn_loose_bomb

# A map with only general spawns would otherwise start the round with no bomb.
execute unless entity @e[tag=mgs.snd_loose_at] at @e[tag=mgs.spawn_point,limit=1] run function mgs:v5.1.0/multiplayer/gamemodes/snd/spawn_loose_bomb

# Last, once everyone is tagged and placed: until then the tick judges nothing, so the gap is never read as a wipe.
scoreboard players set #snd_round_active mgs.data 1

