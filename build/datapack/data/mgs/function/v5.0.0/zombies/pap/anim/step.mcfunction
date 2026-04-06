
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

# Phase: GOING IN (timer 221..237)
execute if score @s mgs.pap_anim matches 221..237 run function mgs:v5.0.0/zombies/pap/anim/going_in

# Trigger: weapon fully in at timer=220 — start inside processing
execute if score @s mgs.pap_anim matches 220 run function mgs:v5.0.0/zombies/pap/anim/trigger_inside

# Phase: INSIDE (timer 161..219)
execute if score @s mgs.pap_anim matches 161..219 run function mgs:v5.0.0/zombies/pap/anim/inside

# Trigger: start coming-out interpolation at timer=160
execute if score @s mgs.pap_anim matches 160 run function mgs:v5.0.0/zombies/pap/anim/trigger_coming_out

# Phase: COMING OUT (timer 146..159)
execute if score @s mgs.pap_anim matches 146..159 run function mgs:v5.0.0/zombies/pap/anim/coming_out

# Trigger: weapon fully emerged at timer=145 — start retreat, allow collection
execute if score @s mgs.pap_anim matches 145 run function mgs:v5.0.0/zombies/pap/anim/trigger_retreat
execute if score @s mgs.pap_anim matches 125 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.1
execute if score @s mgs.pap_anim matches 105 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.1
execute if score @s mgs.pap_anim matches 85 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.1
execute if score @s mgs.pap_anim matches 65 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.1
execute if score @s mgs.pap_anim matches 45 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.1
execute if score @s mgs.pap_anim matches 25 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.1
execute if score @s mgs.pap_anim matches 5 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.1

# Phase: RETREAT (timer 1..115) — smoke particles + looping sound every 20 ticks
execute if score @s mgs.pap_anim matches 1..115 run particle smoke ~ ~0.5 ~ 0.2 0.2 0.2 0.05 2 force
execute store result score #pap_t mgs.data run scoreboard players get @s mgs.pap_anim
scoreboard players operation #pap_t mgs.data %= #20 mgs.data
execute if score @s mgs.pap_anim matches 1..115 if score #pap_t mgs.data matches 0 run function mgs:v5.0.0/zombies/feedback/sound_pap_retreat_loop

# Retreat finished at timer=0 — weapon is lost
execute if score @s mgs.pap_anim matches 0 run function mgs:v5.0.0/zombies/pap/anim/retreat_finish

