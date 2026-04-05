
#> mgs:v5.0.0/zombies/pap/anim_retreat_finish
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/game_tick [ at @s ]
#

# Spawn an item entity and copy the weapon from the display into it (dropping to the ground)
summon minecraft:item ~ ~0.5 ~ {PickupDelay:40,Tags:["mgs.pap_drop"],Item:{id:"minecraft:stone",count:1}}
data modify entity @n[tag=mgs.pap_drop,distance=..1] Item set from entity @n[tag=mgs.pap_weapon_display,distance=..2] item
tag @n[tag=mgs.pap_drop,distance=..1] remove mgs.pap_drop

# Remove weapon display
kill @e[tag=mgs.pap_weapon_display,distance=..2]

# Reset to idle
scoreboard players set @s mgs.pap_anim -1

# Restore static machine display
function mgs:v5.0.0/zombies/pap/anim_restore_display

# Sound
playsound minecraft:entity.generic.extinguish_fire ambient @a[distance=..20] ~ ~ ~ 1.0 0.8

