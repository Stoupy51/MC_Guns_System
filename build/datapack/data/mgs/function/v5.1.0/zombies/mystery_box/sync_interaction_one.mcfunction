
#> mgs:v5.1.0/zombies/mystery_box/sync_interaction_one
#
# @executed	as @e[tag=mgs.mystery_box_pos] & at @s
#
# @within	mgs:v5.1.0/zombies/mystery_box/sync_interaction_visibility [ as @e[tag=mgs.mystery_box_pos] & at @s ]
#

# @s = a box interaction entity, at @s. Decide if it should be reachable.
scoreboard players set #mb_vis mgs.data 0
execute if entity @s[tag=mgs.mystery_box_active] run scoreboard players set #mb_vis mgs.data 1
execute if score #zb_fire_sale_timer mgs.data matches 1.. if entity @s[tag=mgs.mb_fs_active] run scoreboard players set #mb_vis mgs.data 1
execute if entity @n[tag=mgs.mb_display,distance=..3] run scoreboard players set #mb_vis mgs.data 1

execute if score #mb_vis mgs.data matches 1 if entity @s[tag=mgs.mb_hidden] run function mgs:v5.1.0/zombies/mystery_box/interaction_show
execute if score #mb_vis mgs.data matches 0 unless entity @s[tag=mgs.mb_hidden] run function mgs:v5.1.0/zombies/mystery_box/interaction_hide

