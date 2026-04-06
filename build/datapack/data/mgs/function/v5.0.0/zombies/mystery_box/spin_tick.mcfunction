
#> mgs:v5.0.0/zombies/mystery_box/spin_tick
#
# @within	mgs:v5.0.0/zombies/mystery_box/tick
#

# Decrement timer
scoreboard players remove #mb_anim_timer mgs.data 1

# Cycling phase (timer > 0): show random items with staged slowdown cadence
execute if score #mb_anim_timer mgs.data matches 1.. run function mgs:v5.0.0/zombies/mystery_box/cycle_step

# Landing phase (timer = 0): show the result
execute if score #mb_anim_timer mgs.data matches 0 run function mgs:v5.0.0/zombies/mystery_box/show_result

# Pickup window expired (timer = -150): remove display and reset
execute if score #mb_anim_timer mgs.data matches ..-150 run function mgs:v5.0.0/zombies/mystery_box/reset

