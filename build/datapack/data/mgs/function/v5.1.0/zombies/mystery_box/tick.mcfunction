
#> mgs:v5.1.0/zombies/mystery_box/tick
#
# @within	mgs:v5.1.0/zombies/game_tick
#

# Per-box spin animation (the moving bear display is excluded — the move handles it)
execute as @e[tag=mgs.mb_display,tag=!mgs.mb_bear] at @s run function mgs:v5.1.0/zombies/mystery_box/spin_tick_one

# Move animation tick (active box only; never during a Fire Sale)
execute if score #mb_move_timer mgs.data matches 1.. run function mgs:v5.1.0/zombies/mystery_box/move_anim_tick

