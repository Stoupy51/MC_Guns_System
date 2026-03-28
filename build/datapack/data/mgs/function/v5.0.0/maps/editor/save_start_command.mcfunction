
#> mgs:v5.0.0/maps/editor/save_start_command
#
# @executed	as @e[tag=mgs.element.start_command] & at @s
#
# @within	mgs:v5.0.0/maps/editor/save_lists/multiplayer {path:"start_commands"} [ as @e[tag=mgs.element.start_command] & at @s ]
#			mgs:v5.0.0/maps/editor/save_lists/zombies {path:"start_commands"} [ as @e[tag=mgs.element.start_command] & at @s ]
#			mgs:v5.0.0/maps/editor/save_lists/missions {path:"start_commands"} [ as @e[tag=mgs.element.start_command] & at @s ]
#
# @args		path (string)
#

# @s = start command marker, at its position
# Get absolute position
execute store result score #ax mgs.data run data get entity @s Pos[0]
execute store result score #ay mgs.data run data get entity @s Pos[1]
execute store result score #az mgs.data run data get entity @s Pos[2]

# Compute relative coordinates
scoreboard players operation #ax mgs.data -= #base_x mgs.data
scoreboard players operation #ay mgs.data -= #base_y mgs.data
scoreboard players operation #az mgs.data -= #base_z mgs.data

# Build start command entry {pos:[x,y,z],command:"..."}
data modify storage mgs:temp _save_start_cmd set value {pos:[0,0,0],command:""}
execute store result storage mgs:temp _save_start_cmd.pos[0] int 1 run scoreboard players get #ax mgs.data
execute store result storage mgs:temp _save_start_cmd.pos[1] int 1 run scoreboard players get #ay mgs.data
execute store result storage mgs:temp _save_start_cmd.pos[2] int 1 run scoreboard players get #az mgs.data
data modify storage mgs:temp _save_start_cmd.command set from entity @s data.command

# Append to list path
$data modify storage mgs:temp map_edit.map.$(path) append from storage mgs:temp _save_start_cmd

