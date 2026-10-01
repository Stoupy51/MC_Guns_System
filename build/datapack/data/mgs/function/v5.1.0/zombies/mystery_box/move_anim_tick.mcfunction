
#> mgs:v5.1.0/zombies/mystery_box/move_anim_tick
#
# @within	mgs:v5.1.0/zombies/mystery_box/tick
#

scoreboard players remove #mb_move_timer mgs.data 1

execute if score #mb_move_timer mgs.data matches 251 run function mgs:v5.1.0/zombies/mystery_box/move_anim_start_ascend

# Slow, then fast.
execute if score #mb_move_timer mgs.data matches 171..251 run function mgs:v5.1.0/zombies/mystery_box/move_anim_ascend_step

# Only the moving bear and the old box, not the temporary Fire Sale boxes.
execute if score #mb_move_timer mgs.data matches 170 run kill @e[tag=mgs.mb_bear]
execute if score #mb_move_timer mgs.data matches 170 run kill @e[tag=mgs.mb_presence,tag=!mgs.mb_temp]
# A Fire Sale that ended while this bear was the last pull finishes its cleanup now.
execute if score #mb_move_timer mgs.data matches 170 if score #mb_fs_cleanup_pending mgs.data matches 1 unless entity @e[tag=mgs.mb_display] run function mgs:v5.1.0/zombies/mystery_box/fire_sale_cleanup

execute if score #mb_move_timer mgs.data matches 70 run function mgs:v5.1.0/zombies/mystery_box/move_anim_transition

# Fast, then slow.
execute if score #mb_move_timer mgs.data matches 1..69 run function mgs:v5.1.0/zombies/mystery_box/move_anim_descend_step

execute if score #mb_move_timer mgs.data matches 0 run function mgs:v5.1.0/zombies/mystery_box/move_anim_land

