
#> mgs:v5.0.0/zombies/pap/anim/step
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/game_tick [ at @s ]
#

# Decrement timer
scoreboard players remove @s mgs.pap_anim 1

# Trigger: start going-in interpolation (2 ticks after summon for client sync)
execute if score @s mgs.pap_anim matches 238 run function mgs:v5.0.0/zombies/pap/anim/trigger_going_in

# Phase: GOING IN (timer 211..237)
execute if score @s mgs.pap_anim matches 211..237 run function mgs:v5.0.0/zombies/pap/anim/going_in

# Trigger: weapon fully in at timer=210 — start inside processing
execute if score @s mgs.pap_anim matches 210 run function mgs:v5.0.0/zombies/pap/anim/trigger_inside

# Phase: INSIDE (timer 151..209)
execute if score @s mgs.pap_anim matches 151..209 run function mgs:v5.0.0/zombies/pap/anim/inside

# Trigger: start coming-out interpolation at timer=150
execute if score @s mgs.pap_anim matches 150 run function mgs:v5.0.0/zombies/pap/anim/trigger_coming_out

# Phase: COMING OUT (timer 121..149)
execute if score @s mgs.pap_anim matches 121..149 run function mgs:v5.0.0/zombies/pap/anim/coming_out

# Trigger: weapon fully emerged at timer=120 — start retreat, allow collection
execute if score @s mgs.pap_anim matches 120 run function mgs:v5.0.0/zombies/pap/anim/trigger_retreat
execute if score @s mgs.pap_anim matches 119 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.085
execute if score @s mgs.pap_anim matches 100 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.085
execute if score @s mgs.pap_anim matches 80 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.085
execute if score @s mgs.pap_anim matches 60 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.085
execute if score @s mgs.pap_anim matches 40 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.085
execute if score @s mgs.pap_anim matches 20 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.085

# Phase: RETREAT (timer 1..119) — smoke particles
execute if score @s mgs.pap_anim matches 1..119 run particle smoke ~ ~0.5 ~ 0.2 0.2 0.2 0.05 2 force

# Retreat finished at timer=0 — weapon is lost
execute if score @s mgs.pap_anim matches 0 run function mgs:v5.0.0/zombies/pap/anim/retreat_finish

