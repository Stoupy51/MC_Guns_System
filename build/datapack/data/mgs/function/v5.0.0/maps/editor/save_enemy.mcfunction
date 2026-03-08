
#> mgs:v5.0.0/maps/editor/save_enemy
#
# @executed	as @e[tag=mgs.element.enemy] & at @s
#
# @within	mgs:v5.0.0/maps/editor/save_lists/missions [ as @e[tag=mgs.element.enemy] & at @s ]
#

# @s = enemy marker, at its position
# Get absolute position
execute store result score #ax mgs.data run data get entity @s Pos[0]
execute store result score #ay mgs.data run data get entity @s Pos[1]
execute store result score #az mgs.data run data get entity @s Pos[2]

# Compute relative coordinates
scoreboard players operation #ax mgs.data -= #base_x mgs.data
scoreboard players operation #ay mgs.data -= #base_y mgs.data
scoreboard players operation #az mgs.data -= #base_z mgs.data

# Build enemy entry {pos:[x,y,z], function:"..."}
data modify storage mgs:temp _save_enemy set value {pos:[0,0,0],function:""}
execute store result storage mgs:temp _save_enemy.pos[0] int 1 run scoreboard players get #ax mgs.data
execute store result storage mgs:temp _save_enemy.pos[1] int 1 run scoreboard players get #ay mgs.data
execute store result storage mgs:temp _save_enemy.pos[2] int 1 run scoreboard players get #az mgs.data
data modify storage mgs:temp _save_enemy.function set from entity @s data.function

# Append to enemies list
data modify storage mgs:temp map_edit.map.enemies append from storage mgs:temp _save_enemy

