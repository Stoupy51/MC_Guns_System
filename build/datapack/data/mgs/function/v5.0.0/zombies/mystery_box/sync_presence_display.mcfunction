
#> mgs:v5.0.0/zombies/mystery_box/sync_presence_display
#
# @within	mgs:v5.0.0/zombies/mystery_box/setup_positions
#			mgs:v5.0.0/zombies/mystery_box/move_active_position
#

# Keep one chest display at the currently active mystery box.
kill @e[tag=mgs.mb_presence]
execute as @n[tag=mgs.mystery_box_active] at @s run summon minecraft:item_display ~ ~0.7 ~ {Tags:["mgs.mb_presence","mgs.gm_entity"],item_display:"fixed",billboard:"fixed",item:{id:"minecraft:chest",count:1},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.85f,0.85f,0.85f]}}

