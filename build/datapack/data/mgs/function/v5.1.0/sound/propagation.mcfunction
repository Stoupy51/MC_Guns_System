
#> mgs:v5.1.0/sound/propagation
#
# @executed	as @a[distance=0.001..224] & facing entity @s eyes
#
# @within	mgs:v5.1.0/sound/acoustics_main [ as @a[distance=0.001..224] & facing entity @s eyes ]
#

scoreboard players operation #processed_acoustics mgs.data = #origin_acoustics_level mgs.data
scoreboard players operation #attenuation_acoustics mgs.data = #origin_acoustics_level mgs.data
scoreboard players add #attenuation_acoustics mgs.data 1

# One level closer when the source (0-4) is above the listener's level: enclosed spaces make distant sounds seem near.
execute if score #origin_acoustics_level mgs.data matches 0..4 if score #origin_acoustics_level mgs.data > @s mgs.acoustics_level run scoreboard players remove #processed_acoustics mgs.data 1

# One level louder when the source is below: a more reflective spot sounds louder.
execute if score #origin_acoustics_level mgs.data < @s mgs.acoustics_level run scoreboard players add #processed_acoustics mgs.data 1

# Again when source + 1 is still below, which smooths the transition between environments.
execute if score #attenuation_acoustics mgs.data < @s mgs.acoustics_level run scoreboard players add #processed_acoustics mgs.data 1

# A listener in water (5) always hears the water level.
execute if score @s mgs.acoustics_level matches 5 run scoreboard players set #processed_acoustics mgs.data 5

execute if score #processed_acoustics mgs.data matches 0 run function mgs:v5.1.0/sound/hearing/0_distant with storage mgs:gun all.sounds
execute if score #processed_acoustics mgs.data matches 1 run function mgs:v5.1.0/sound/hearing/1_far with storage mgs:gun all.sounds
execute if score #processed_acoustics mgs.data matches 2 run function mgs:v5.1.0/sound/hearing/2_midrange with storage mgs:gun all.sounds
execute if score #processed_acoustics mgs.data matches 3 run function mgs:v5.1.0/sound/hearing/3_near with storage mgs:gun all.sounds
execute if score #processed_acoustics mgs.data matches 4 run function mgs:v5.1.0/sound/hearing/4_closest with storage mgs:gun all.sounds
execute if score #processed_acoustics mgs.data matches 5 run function mgs:v5.1.0/sound/hearing/5_water with storage mgs:gun all.sounds

