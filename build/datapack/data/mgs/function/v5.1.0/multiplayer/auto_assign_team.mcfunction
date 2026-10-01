
#> mgs:v5.1.0/multiplayer/auto_assign_team
#
# @executed	as @a[scores={mgs.mp.in_game=1}]
#
# @within	mgs:v5.1.0/multiplayer/start [ as @a[scores={mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/join_game
#			mgs:v5.1.0/multiplayer/gamemodes/tdm/setup [ as @a[scores={mgs.mp.in_game=1,mgs.mp.team=0}] ]
#			dialog mgs:v5.1.0/multiplayer/setup
#

# FFA: everyone goes to the single FFA team instead of being split red and blue.
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run return run function mgs:v5.1.0/multiplayer/join_ffa

execute store result score #red_count mgs.data if entity @a[scores={mgs.mp.team=1}]
execute store result score #blue_count mgs.data if entity @a[scores={mgs.mp.team=2}]

# The player's own team does not count, so re-running auto-assign stays stable instead of clumping onto one side.
execute if score @s mgs.mp.team matches 1 run scoreboard players remove #red_count mgs.data 1
execute if score @s mgs.mp.team matches 2 run scoreboard players remove #blue_count mgs.data 1

# The smaller team, red when tied.
execute if score #red_count mgs.data <= #blue_count mgs.data run function mgs:v5.1.0/multiplayer/join_red
execute if score #red_count mgs.data > #blue_count mgs.data run function mgs:v5.1.0/multiplayer/join_blue

