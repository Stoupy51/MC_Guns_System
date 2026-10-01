
#> mgs:v5.1.0/zombies/mystery_box/spin_tick_one
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.1.0/zombies/mystery_box/tick [ as @e[tag=...] & at @s ]
#

scoreboard players remove @s mgs.mb.anim 1

# Timeslip: 2x spin speed, only inside the cycling phase (1..103) so the float-up at 104 still runs;
# anim stays even, so the doubled step lands exactly on 0 and never reaches the reset window.
execute if score @s mgs.mb.timeslip matches 1 if score @s mgs.mb.anim matches 1..103 run scoreboard players remove @s mgs.mb.anim 1

# One tick after spawn, which avoids same-tick interpolation glitches.
execute if score @s mgs.mb.anim matches 104 run data merge entity @s {transformation:{translation:[0f,0.8f,0f]},start_interpolation:0,interpolation_duration:200}

# Random items, slowing down in stages.
execute if score @s mgs.mb.anim matches 1.. run function mgs:v5.1.0/zombies/mystery_box/cycle_step_one

execute if score @s mgs.mb.anim matches 0 run function mgs:v5.1.0/zombies/mystery_box/show_result_one

# The pickup window ends at -150.
execute if score @s mgs.mb.anim matches ..-150 run function mgs:v5.1.0/zombies/mystery_box/reset_one

