
#> mgs:v5.1.0/zombies/mystery_box/tick
#
# @within	mgs:v5.1.0/zombies/game_tick
#

# The moving bear display belongs to the move animation.
execute as @e[tag=mgs.mb_display,tag=!mgs.mb_bear] at @s run function mgs:v5.1.0/zombies/mystery_box/spin_tick_one

# Active box only, never during a Fire Sale.
execute if score #mb_move_timer mgs.data matches 1.. run function mgs:v5.1.0/zombies/mystery_box/move_anim_tick

