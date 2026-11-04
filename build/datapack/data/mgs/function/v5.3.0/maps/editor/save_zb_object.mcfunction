
#> mgs:v5.3.0/maps/editor/save_zb_object
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/maps/editor/save_lists/zombies {etype:"player_spawn_zb"} [ as @e[tag=mgs.element.player_spawn_zb] & at @s ]
#			mgs:v5.3.0/maps/editor/save_lists/zombies {etype:"zombie_spawn"} [ as @e[tag=mgs.element.zombie_spawn] & at @s ]
#			mgs:v5.3.0/maps/editor/save_lists/zombies {etype:"wallbuy"} [ as @e[tag=mgs.element.wallbuy] & at @s ]
#			mgs:v5.3.0/maps/editor/save_lists/zombies {etype:"door"} [ as @e[tag=mgs.element.door] & at @s ]
#			mgs:v5.3.0/maps/editor/save_lists/zombies {etype:"trap"} [ as @e[tag=mgs.element.trap] & at @s ]
#			mgs:v5.3.0/maps/editor/save_lists/zombies {etype:"perk_machine"} [ at @s ]
#			mgs:v5.3.0/maps/editor/save_lists/zombies {etype:"mystery_box_pos"} [ as @e[tag=mgs.element.mystery_box_pos] & at @s ]
#			mgs:v5.3.0/maps/editor/save_lists/zombies {etype:"power_switch"} [ as @e[tag=mgs.element.power_switch] & at @s ]
#			mgs:v5.3.0/maps/editor/save_lists/zombies {etype:"pap_machine"} [ at @s ]
#			mgs:v5.3.0/maps/editor/save_lists/zombies {etype:"special_spawn"} [ as @e[tag=mgs.element.special_spawn] & at @s ]
#			mgs:v5.3.0/maps/editor/save_lists/zombies {etype:"barricade"} [ as @e[tag=mgs.element.barricade] & at @s ]
#			mgs:v5.3.0/maps/editor/save_lists/zombies {etype:"wunderfizz"} [ as @e[tag=mgs.element.wunderfizz] & at @s ]
#
# @args		etype (string)
#

# Run as the marker, at it.
execute store result score #ax mgs.data run data get entity @s Pos[0]
execute store result score #ay mgs.data run data get entity @s Pos[1]
execute store result score #az mgs.data run data get entity @s Pos[2]

scoreboard players operation #ax mgs.data -= #base_x mgs.data
scoreboard players operation #ay mgs.data -= #base_y mgs.data
scoreboard players operation #az mgs.data -= #base_z mgs.data

# The marker's data is the base entry.
data modify storage mgs:temp _save_zb set from entity @s data

# pos becomes relative.
data modify storage mgs:temp _save_zb.pos set value [0, 0, 0]
execute store result storage mgs:temp _save_zb.pos[0] int 1 run scoreboard players get #ax mgs.data
execute store result storage mgs:temp _save_zb.pos[1] int 1 run scoreboard players get #ay mgs.data
execute store result storage mgs:temp _save_zb.pos[2] int 1 run scoreboard players get #az mgs.data

# Yaw rounded to whole degrees from 0 to 359, left out at 0 (3600 keeps a negative yaw positive). The rotation a marker of an older map carries is rebuilt on load.
execute store result score #yaw mgs.data run data get entity @s data.yaw 10
scoreboard players add #yaw mgs.data 3605
scoreboard players operation #yaw mgs.data /= #10 mgs.data
scoreboard players operation #yaw mgs.data %= #360 mgs.data
data remove storage mgs:temp _save_zb.yaw
data remove storage mgs:temp _save_zb.rotation
execute unless score #yaw mgs.data matches 0 store result storage mgs:temp _save_zb.yaw int 1 run scoreboard players get #yaw mgs.data

# The editor's own data, and the element's name back from title (see AXIOM_KEYS).
data remove storage mgs:temp _save_zb._disp_sig
data remove storage mgs:temp _save_zb._ed
data remove storage mgs:temp _save_zb.name
data remove storage mgs:temp _save_zb.min
data remove storage mgs:temp _save_zb.max
execute if data storage mgs:temp _save_zb.title run data modify storage mgs:temp _save_zb.name set from storage mgs:temp _save_zb.title
data remove storage mgs:temp _save_zb.title
$function mgs:v5.3.0/maps/compact/$(etype)

