
#> mgs:v5.0.0/multiplayer/assign_pid
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# Assign a unique player ID
scoreboard players operation @s mgs.mp.pid = #next_pid mgs.data
scoreboard players add #next_pid mgs.data 1

# Initialize player data entry in storage
data modify storage mgs:temp _new_player set value {pid:0,favorites:[],liked:[],default_loadout:0}
execute store result storage mgs:temp _new_player.pid int 1 run scoreboard players get @s mgs.mp.pid
data modify storage mgs:multiplayer player_data append from storage mgs:temp _new_player

