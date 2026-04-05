
#> mgs:v5.0.0/zombies/pap/anim_step
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/game_tick [ at @s ]
#

# Decrement timer
scoreboard players remove @s mgs.pap_anim 1

# Phase: GOING IN (timer 170..199)
execute if score @s mgs.pap_anim matches 170..199 run function mgs:v5.0.0/zombies/pap/anim_going_in

# Phase: INSIDE (timer 130..169)
execute if score @s mgs.pap_anim matches 130..169 run function mgs:v5.0.0/zombies/pap/anim_inside

# Trigger: start coming-out interpolation at timer=129 (first tick of coming-out)
execute if score @s mgs.pap_anim matches 129 run function mgs:v5.0.0/zombies/pap/anim_trigger_coming_out

# Phase: COMING OUT (timer 100..129)
execute if score @s mgs.pap_anim matches 100..129 run function mgs:v5.0.0/zombies/pap/anim_coming_out

# Trigger: weapon fully emerged — immediately start retreat (CoD style, at timer=100)
execute if score @s mgs.pap_anim matches 100 run function mgs:v5.0.0/zombies/pap/anim_trigger_retreat

