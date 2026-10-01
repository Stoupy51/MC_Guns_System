
#> mgs:v5.1.0/zombies/pap/anim/step
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/game_tick [ at @s ]
#			mgs:v5.1.0/zombies/pap/anim/step_timeslip
#

scoreboard players remove @s mgs.pap_anim 1

execute if score @s mgs.pap_anim matches 298 run function mgs:v5.1.0/zombies/pap/anim/trigger_going_in

execute if score @s mgs.pap_anim matches 281..297 run function mgs:v5.1.0/zombies/pap/anim/going_in

execute if score @s mgs.pap_anim matches 280 run function mgs:v5.1.0/zombies/pap/anim/trigger_inside

execute if score @s mgs.pap_anim matches 225..279 run function mgs:v5.1.0/zombies/pap/anim/inside

execute if score @s mgs.pap_anim matches 252 run function mgs:v5.1.0/zombies/pap/anim/apply_cosmetics

execute if score @s mgs.pap_anim matches 225 run function mgs:v5.1.0/zombies/pap/anim/trigger_coming_out

execute if score @s mgs.pap_anim matches 206..219 run function mgs:v5.1.0/zombies/pap/anim/coming_out

execute if score @s mgs.pap_anim matches 205 run function mgs:v5.1.0/zombies/pap/anim/trigger_retreat
execute if score @s mgs.pap_anim matches 205 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04
execute if score @s mgs.pap_anim matches 185 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04
execute if score @s mgs.pap_anim matches 165 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04
execute if score @s mgs.pap_anim matches 145 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04
execute if score @s mgs.pap_anim matches 125 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04
execute if score @s mgs.pap_anim matches 105 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04
execute if score @s mgs.pap_anim matches 85 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04
execute if score @s mgs.pap_anim matches 65 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04
execute if score @s mgs.pap_anim matches 45 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04
execute if score @s mgs.pap_anim matches 25 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04
execute if score @s mgs.pap_anim matches 5 as @n[tag=mgs.pap_weapon_display,distance=..2] at @s run tp @s ^ ^ ^-0.04

# Smoke and a looping sound every 20 ticks while retreating.
execute if score @s mgs.pap_anim matches 1..205 positioned ~ ~-2 ~ run particle smoke ~ ~0.5 ~ 0.2 0.2 0.2 0.05 2 force @a[distance=..48]
execute store result score #pap_t mgs.data run scoreboard players get @s mgs.pap_anim
scoreboard players operation #pap_t mgs.data %= #20 mgs.data
execute if score @s mgs.pap_anim matches 1..205 if score #pap_t mgs.data matches 0 run playsound mgs:zombies/pap/retreat_loop ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.5 1.0

execute if score @s mgs.pap_anim matches 0 run function mgs:v5.1.0/zombies/pap/anim/retreat_finish

