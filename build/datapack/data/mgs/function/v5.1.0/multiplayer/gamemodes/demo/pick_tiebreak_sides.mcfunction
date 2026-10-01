
#> mgs:v5.1.0/multiplayer/gamemodes/demo/pick_tiebreak_sides
#
# @executed	as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/next_round
#

# mp.kills is per player and only zeroed by multiplayer/start.
scoreboard players set #demo_kills_red mgs.data 0
scoreboard players set #demo_kills_blue mgs.data 0
execute as @a[scores={mgs.mp.team=1}] run scoreboard players operation #demo_kills_red mgs.data += @s mgs.mp.kills
execute as @a[scores={mgs.mp.team=2}] run scoreboard players operation #demo_kills_blue mgs.data += @s mgs.mp.kills

# A tie leaves Red attacking, like the side-picking fallback.
scoreboard players set #demo_attackers mgs.data 1
execute if score #demo_kills_red mgs.data > #demo_kills_blue mgs.data run scoreboard players set #demo_attackers mgs.data 2

# start_round announces the defenders, so only the tie case is spelled out.
tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.kills_2","color":"gray"},{"translate":"mgs.red_2","color":"red"},{"score":{"name":"#demo_kills_red","objective":"mgs.data"},"color":"white"},{"text":" - ","color":"gray"},{"translate":"mgs.blue_2","color":"blue"},{"score":{"name":"#demo_kills_blue","objective":"mgs.data"},"color":"white"}]
execute if score #demo_kills_red mgs.data = #demo_kills_blue mgs.data run tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.kills_are_level_so","color":"yellow"},{"translate":"mgs.blue","color":"blue"},[{"text":" ","color":"yellow"}, {"translate":"mgs.defends"}]]

