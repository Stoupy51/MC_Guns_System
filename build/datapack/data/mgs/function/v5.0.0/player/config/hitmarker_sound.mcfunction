
#> mgs:v5.0.0/player/config/hitmarker_sound
#
# @within	#mgs:signals/damage
#

# Play hitmarker sound to the shooter if their personal config has it enabled
# For hitscan: shooter has tag mgs.ticking
execute as @a[tag=mgs.ticking] if score @s mgs.player.hitmarker matches 1 at @s run playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.5 2.0
# For explosions: shooter has tag mgs.temp_shooter (skip if already played via ticking)
execute as @a[tag=mgs.temp_shooter,tag=!mgs.ticking] if score @s mgs.player.hitmarker matches 1 at @s run playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.5 2.0

