
#> mgs:v5.1.0/multiplayer/gamemodes/demo/start_round
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/setup
#			mgs:v5.1.0/multiplayer/gamemodes/demo/next_round 60t [ scheduled ]
#

# Guard: only while the game is running (a scheduled call may fire after the game ended)
execute if data storage mgs:multiplayer game{state:"lobby"} run return fail
execute if data storage mgs:multiplayer game{state:"ended"} run return fail

# Announce round. The decider is announced as one, but plays like any other round.
tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],[{"text":"────── ","color":"gold"}, {"translate":"mgs.round"}],{"score":{"name":"#demo_round","objective":"mgs.data"},"color":"yellow"},{"text":" ──────","color":"gold"}]
execute if score #demo_round mgs.data matches 3.. run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"⚡ ",{"translate":"mgs.tie_break_round_most_kills_defends","color":"gold","bold":true}]
execute if score #demo_attackers mgs.data matches 1 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.red","color":"red"},[{"text":" "}, {"translate":"mgs.attacks_both_sites"}, " | "],{"translate":"mgs.blue","color":"blue"},[{"text":" "}, {"translate":"mgs.defends_2"}]]
execute if score #demo_attackers mgs.data matches 2 run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.blue","color":"blue"},[{"text":" "}, {"translate":"mgs.attacks_both_sites"}, " | "],{"translate":"mgs.red","color":"red"},[{"text":" "}, {"translate":"mgs.defends_2"}]]
playsound minecraft:block.note_block.harp player @a ~ ~ ~ 1 1.0

# Every site back to intact
kill @e[tag=mgs.demo_bomb]
kill @e[tag=mgs.demo_bomb_vis]
kill @e[tag=mgs.demo_bomb_hud]
kill @e[tag=mgs.demo_wreck]
kill @e[tag=mgs.demo_rubble]
scoreboard players set @e[tag=mgs.demo_obj] mgs.demo_state 0
scoreboard players set @e[tag=mgs.demo_obj] mgs.demo_prog 0
scoreboard players set @e[tag=mgs.demo_obj] mgs.demo_fuse 0
scoreboard players set @e[tag=mgs.demo_obj] mgs.demo_owner 0
execute as @e[tag=mgs.demo_obj] at @s run function mgs:v5.1.0/multiplayer/gamemodes/demo/restore_site

# Clock, same length every round; it stops while a bomb is down, which is why this mode owns #mp_timer.
scoreboard players set #demo_timer mgs.data 3600
scoreboard players operation #mp_timer mgs.data = #demo_timer mgs.data

# Who is carrying a bomb. Every attacker is, on every respawn, which is why Demolition needs none of the
# carry/drop/pickup machinery S&D has — the tag IS the bomb.
tag @a remove mgs.demo_atk
execute if score #demo_attackers mgs.data matches 1 run tag @a[scores={mgs.mp.team=1}] add mgs.demo_atk
execute if score #demo_attackers mgs.data matches 2 run tag @a[scores={mgs.mp.team=2}] add mgs.demo_atk

# Everyone alive and back at their spawns. Mid-respawn spectators are pulled out of it and their countdown
# is cleared, so a death from the previous round cannot respawn them a second time mid-round.
execute as @a[scores={mgs.mp.team=1..2},gamemode=spectator] run spectate @s
gamemode adventure @a[scores={mgs.mp.team=1..2},gamemode=spectator]
scoreboard players set @a[scores={mgs.mp.team=1..2}] mgs.mp.spectate_timer 0
execute as @a[scores={mgs.mp.team=1}] at @s run function mgs:v5.1.0/multiplayer/pick_spawn {type:"red"}
execute as @a[scores={mgs.mp.team=2}] at @s run function mgs:v5.1.0/multiplayer/pick_spawn {type:"blue"}
tag @e[tag=mgs.spawn_used] remove mgs.spawn_used
execute as @a[scores={mgs.mp.team=1..2}] at @s run function mgs:v5.1.0/multiplayer/apply_class

# Open the round LAST, once the sites are intact and everyone is placed
scoreboard players set #demo_round_active mgs.data 1

