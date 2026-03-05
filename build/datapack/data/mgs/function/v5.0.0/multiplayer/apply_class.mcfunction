
#> mgs:v5.0.0/multiplayer/apply_class
#
# @executed	as @a & at @s
#
# @within	mgs:v5.0.0/multiplayer/start [ as @a & at @s ]
#			mgs:v5.0.0/multiplayer/prep_tick [ at @s ]
#			mgs:v5.0.0/multiplayer/gamemodes/snd/start_round [ as @a[scores={mgs.mp.team=1..2}] & at @s ]
#			mgs:v5.0.0/multiplayer/on_respawn
#			mgs:v5.0.0/multiplayer/auto_apply_default
#

# Check for custom loadout (negative mp.class = custom loadout ID)
execute if score @s mgs.mp.class matches ..-1 run return run function mgs:v5.0.0/multiplayer/apply_custom_class

# Standard class lookup by class_num score
execute if score @s mgs.mp.class matches 1 run data modify storage mgs:temp current_class set from storage mgs:multiplayer classes_list[0]
execute if score @s mgs.mp.class matches 2 run data modify storage mgs:temp current_class set from storage mgs:multiplayer classes_list[1]
execute if score @s mgs.mp.class matches 3 run data modify storage mgs:temp current_class set from storage mgs:multiplayer classes_list[2]
execute if score @s mgs.mp.class matches 4 run data modify storage mgs:temp current_class set from storage mgs:multiplayer classes_list[3]
execute if score @s mgs.mp.class matches 5 run data modify storage mgs:temp current_class set from storage mgs:multiplayer classes_list[4]
execute if score @s mgs.mp.class matches 6 run data modify storage mgs:temp current_class set from storage mgs:multiplayer classes_list[5]
execute if score @s mgs.mp.class matches 7 run data modify storage mgs:temp current_class set from storage mgs:multiplayer classes_list[6]
execute if score @s mgs.mp.class matches 8 run data modify storage mgs:temp current_class set from storage mgs:multiplayer classes_list[7]
execute if score @s mgs.mp.class matches 9 run data modify storage mgs:temp current_class set from storage mgs:multiplayer classes_list[8]
execute if score @s mgs.mp.class matches 10 run data modify storage mgs:temp current_class set from storage mgs:multiplayer classes_list[9]

# Apply the loadout dynamically from the selected class
function mgs:v5.0.0/multiplayer/apply_class_dynamic

