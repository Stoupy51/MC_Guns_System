
#> mgs:v5.0.0/zombies/pap/anim/retreat_finish
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/pap/anim/step
#

# Weapon is lost — destroy it (not dropped)
kill @e[tag=mgs.pap_weapon_display,distance=..2]

# Reset to idle
scoreboard players set @s mgs.pap_anim -1

# Notify and sound
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.the_weapon_was_lost","color":"red","bold":true}]
playsound minecraft:entity.generic.extinguish_fire ambient @a[distance=..20] ~ ~ ~ 1.0 0.8

# Clean up orphaned magazine and PAP tracking for the owner
execute store result score #pap_mid mgs.data run scoreboard players get @s mgs.zb.pap.id
execute store result storage mgs:temp _pap_retreat.id int 1 run scoreboard players get @s mgs.zb.pap.id
function mgs:v5.0.0/zombies/pap/retreat_cleanup with storage mgs:temp _pap_retreat

