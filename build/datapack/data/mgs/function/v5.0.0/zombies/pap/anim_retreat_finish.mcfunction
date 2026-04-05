
#> mgs:v5.0.0/zombies/pap/anim_retreat_finish
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/game_tick [ at @s ]
#

# Weapon is lost — destroy it (not dropped)
kill @e[tag=mgs.pap_weapon_display,distance=..2]

# Reset to idle
scoreboard players set @s mgs.pap_anim -1

# Restore static machine display
function mgs:v5.0.0/zombies/pap/anim_restore_display

# Notify and sound
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.the_weapon_was_lost","color":"red","bold":true}]
playsound minecraft:entity.generic.extinguish_fire ambient @a[distance=..20] ~ ~ ~ 1.0 0.8

