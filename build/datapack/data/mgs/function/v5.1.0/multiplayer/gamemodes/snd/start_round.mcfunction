
#> mgs:v5.1.0/multiplayer/gamemodes/snd/start_round
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/setup
#			mgs:v5.1.0/multiplayer/gamemodes/snd/next_round 60t [ scheduled ]
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
scoreboard players set #snd_round_timer mgs.data 3000

# Restore players who died last round (S&D deaths skip the respawn countdown)
execute as @a[scores={mgs.mp.team=1..2},gamemode=spectator] run spectate @s
gamemode adventure @a[scores={mgs.mp.team=1..2},gamemode=spectator]

# Tag alive players
tag @a[scores={mgs.mp.team=1..2},gamemode=!spectator] add mgs.snd_alive

# Teleport everyone to their team spawns and re-apply class loadouts
execute as @a[scores={mgs.mp.team=1}] at @s run function mgs:v5.1.0/multiplayer/pick_spawn {type:"red"}
execute as @a[scores={mgs.mp.team=2}] at @s run function mgs:v5.1.0/multiplayer/pick_spawn {type:"blue"}
tag @e[tag=mgs.spawn_used] remove mgs.spawn_used
execute as @a[scores={mgs.mp.team=1..2}] at @s run function mgs:v5.1.0/multiplayer/apply_class

# Drop a fresh bomb in front of the attacking team. There is exactly ONE bomb per round and nobody starts
# holding it, so the attackers' first job is to collect it — that walk is what gives the defenders time
# to set up, and it is the main thing that separates this from a Counter-Strike round.
tag @a remove mgs.snd_carrier
kill @e[tag=mgs.snd_loose]
kill @e[tag=mgs.snd_carrier_label]
execute if score #snd_attackers mgs.data matches 1 at @e[tag=mgs.spawn_red,limit=1] run function mgs:v5.1.0/multiplayer/gamemodes/snd/spawn_loose_bomb
execute if score #snd_attackers mgs.data matches 2 at @e[tag=mgs.spawn_blue,limit=1] run function mgs:v5.1.0/multiplayer/gamemodes/snd/spawn_loose_bomb

# Safety net: a map defining only general spawns would otherwise open the round with no bomb anywhere,
# which the attackers could never win. Any spawn point is better than none.
execute unless entity @e[tag=mgs.snd_loose_at] at @e[tag=mgs.spawn_point,limit=1] run function mgs:v5.1.0/multiplayer/gamemodes/snd/spawn_loose_bomb

# Open the round LAST, once everyone is alive-tagged and placed. Until this is 1 the tick judges nothing,
# so the gap between rounds can never be mistaken for a team wipe.
scoreboard players set #snd_round_active mgs.data 1

