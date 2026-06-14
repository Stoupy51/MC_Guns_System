
#> mgs:v5.0.1/zombies/mystery_box/spin_tick_one
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.0.1/zombies/mystery_box/tick [ as @e[tag=...] & at @s ]
#

scoreboard players remove @s mgs.mb.anim 1

# Start the float-up one tick after spawn (avoids same-tick interpolation glitches)
execute if score @s mgs.mb.anim matches 104 run data merge entity @s {transformation:{translation:[0f,0.8f,0f]},start_interpolation:0,interpolation_duration:200}

# Cycling phase (anim > 0): show random items with staged slowdown cadence
execute if score @s mgs.mb.anim matches 1.. run function mgs:v5.0.1/zombies/mystery_box/cycle_step_one

# Landing (anim == 0): decide + show the result
execute if score @s mgs.mb.anim matches 0 run function mgs:v5.0.1/zombies/mystery_box/show_result_one

# Pickup window expired (anim == -150): remove display and reset this box
execute if score @s mgs.mb.anim matches ..-150 run function mgs:v5.0.1/zombies/mystery_box/reset_one

