
#> mgs:v5.0.0/zombies/mystery_box/sync_presence_display
#
# @within	mgs:v5.0.0/zombies/mystery_box/setup_positions
#

# Keep one chest display at the currently active mystery box.
kill @e[tag=mgs.mb_presence]
execute as @n[tag=mgs.mystery_box_active] at @s run data modify storage mgs:temp _mb_chest.yaw set value 0.0f
execute as @n[tag=mgs.mystery_box_active] at @s run data modify storage mgs:temp _mb_chest.yaw set from entity @s Rotation[0]
execute as @n[tag=mgs.mystery_box_active] at @s run function mgs:v5.0.0/zombies/mystery_box/summon_presence_display with storage mgs:temp _mb_chest

