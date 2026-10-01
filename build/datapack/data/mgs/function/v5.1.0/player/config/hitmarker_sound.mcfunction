
#> mgs:v5.1.0/player/config/hitmarker_sound
#
# @within	#mgs:signals/damage
#

execute as @a[tag=mgs.ticking] if score @s mgs.player.hitmarker matches 1 at @s run playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1.0 2.0
# Skipped when already played through ticking.
execute as @a[tag=mgs.temp_shooter,tag=!mgs.ticking] if score @s mgs.player.hitmarker matches 1 at @s run playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1.0 2.0

