
#> mgs:v5.0.0/zombies/mystery_box/move_anim_tick
#
# @within	mgs:v5.0.0/zombies/mystery_box/tick
#

scoreboard players remove #mb_move_timer mgs.data 1

# Bear phase: start ascend interpolation on chest + bear
execute if score #mb_move_timer mgs.data matches 251 run function mgs:v5.0.0/zombies/mystery_box/move_anim_start_ascend

# Ascend phase: move chest + bear upward (slow then fast)
execute if score #mb_move_timer mgs.data matches 171..251 run function mgs:v5.0.0/zombies/mystery_box/move_anim_ascend_step

# End of ascend: kill old displays
execute if score #mb_move_timer mgs.data matches 170 run kill @e[tag=mgs.mb_display]
execute if score #mb_move_timer mgs.data matches 170 run kill @e[tag=mgs.mb_presence]

# Wait phase (170..71): 5 seconds, no box visible

# Transition: pick new location, spawn descending chest
execute if score #mb_move_timer mgs.data matches 70 run function mgs:v5.0.0/zombies/mystery_box/move_anim_transition

# Descend phase: chest descends at new location (fast then slow)
execute if score #mb_move_timer mgs.data matches 1..69 run function mgs:v5.0.0/zombies/mystery_box/move_anim_descend_step

# Land: finalize
execute if score #mb_move_timer mgs.data matches 0 run function mgs:v5.0.0/zombies/mystery_box/move_anim_land

