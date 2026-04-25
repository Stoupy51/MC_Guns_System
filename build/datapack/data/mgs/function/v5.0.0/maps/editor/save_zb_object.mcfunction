
#> mgs:v5.0.0/maps/editor/save_zb_object
#
# @executed	as @e[tag=mgs.element.player_spawn_zb] & at @s
#
# @within	mgs:v5.0.0/maps/editor/save_lists/zombies {path:"spawning_points.players"} [ as @e[tag=mgs.element.player_spawn_zb] & at @s ]
#			mgs:v5.0.0/maps/editor/save_lists/zombies {path:"spawning_points.zombies"} [ as @e[tag=mgs.element.zombie_spawn] & at @s ]
#			mgs:v5.0.0/maps/editor/save_lists/zombies {path:"wallbuys"} [ as @e[tag=mgs.element.wallbuy] & at @s ]
#			mgs:v5.0.0/maps/editor/save_lists/zombies {path:"doors"} [ as @e[tag=mgs.element.door] & at @s ]
#			mgs:v5.0.0/maps/editor/save_lists/zombies {path:"traps"} [ as @e[tag=mgs.element.trap] & at @s ]
#			mgs:v5.0.0/maps/editor/save_lists/zombies {path:"perks"} [ at @s ]
#			mgs:v5.0.0/maps/editor/save_lists/zombies {path:"mystery_box.positions"} [ as @e[tag=mgs.element.mystery_box_pos] & at @s ]
#			mgs:v5.0.0/maps/editor/save_lists/zombies {path:"power_switch"} [ as @e[tag=mgs.element.power_switch] & at @s ]
#			mgs:v5.0.0/maps/editor/save_lists/zombies {path:"pap_machines"} [ at @s ]
#			mgs:v5.0.0/maps/editor/save_lists/zombies {path:"barriers"} [ as @e[tag=mgs.element.barrier] & at @s ]
#
# @args		path (string)
#

# @s = marker entity, at its position
# Get absolute position
execute store result score #ax mgs.data run data get entity @s Pos[0]
execute store result score #ay mgs.data run data get entity @s Pos[1]
execute store result score #az mgs.data run data get entity @s Pos[2]

# Compute relative coordinates
scoreboard players operation #ax mgs.data -= #base_x mgs.data
scoreboard players operation #ay mgs.data -= #base_y mgs.data
scoreboard players operation #az mgs.data -= #base_z mgs.data

# Copy marker's data compound as the base entry
data modify storage mgs:temp _save_zb set from entity @s data

# Overwrite pos with relative coordinates
data modify storage mgs:temp _save_zb.pos set value [0, 0, 0]
execute store result storage mgs:temp _save_zb.pos[0] int 1 run scoreboard players get #ax mgs.data
execute store result storage mgs:temp _save_zb.pos[1] int 1 run scoreboard players get #ay mgs.data
execute store result storage mgs:temp _save_zb.pos[2] int 1 run scoreboard players get #az mgs.data

# Build rotation array from yaw (pitch is always 0)
data modify storage mgs:temp _save_zb.rotation set value [0.0f, 0.0f]
data modify storage mgs:temp _save_zb.rotation[0] set from entity @s data.yaw

# Remove internal-only marker fields (yaw is stored in rotation array)
data remove storage mgs:temp _save_zb.yaw

# Append to the correct list
$data modify storage mgs:temp map_edit.map.$(path) append from storage mgs:temp _save_zb

