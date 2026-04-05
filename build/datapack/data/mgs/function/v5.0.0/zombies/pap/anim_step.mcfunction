
#> mgs:v5.0.0/zombies/pap/anim_step
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/game_tick [ at @s ]
#

# Decrement timer
scoreboard players remove @s mgs.pap_anim 1

# Phase: GOING IN (timer 200..239)
execute if score @s mgs.pap_anim matches 200..239 run function mgs:v5.0.0/zombies/pap/anim_going_in

# Trigger: weapon fully in at timer=199 — start inside rotation
execute if score @s mgs.pap_anim matches 199 run function mgs:v5.0.0/zombies/pap/anim_trigger_inside

# Phase: INSIDE (timer 140..199)
execute if score @s mgs.pap_anim matches 140..199 run function mgs:v5.0.0/zombies/pap/anim_inside

# Trigger: start coming-out interpolation at timer=139
execute if score @s mgs.pap_anim matches 139 run function mgs:v5.0.0/zombies/pap/anim_trigger_coming_out

# Phase: COMING OUT (timer 100..139)
execute if score @s mgs.pap_anim matches 100..139 run function mgs:v5.0.0/zombies/pap/anim_coming_out

# Trigger: weapon fully emerged at timer=100 — start retreat
execute if score @s mgs.pap_anim matches 100 run function mgs:v5.0.0/zombies/pap/anim_trigger_retreat

