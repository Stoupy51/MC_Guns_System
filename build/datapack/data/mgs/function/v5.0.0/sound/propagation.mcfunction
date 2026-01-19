
#> mgs:v5.0.0/sound/propagation
#
# @executed	as @a[distance=0.001..224] & facing entity @s eyes
#
# @within	mgs:v5.0.0/sound/acoustics_main [ as @a[distance=0.001..224] & facing entity @s eyes ]
#

# Make copies of the original acoustics level to work on
scoreboard players operation #processed_acoustics mgs.data = #origin_acoustics_level mgs.data
scoreboard players operation #attenuation_acoustics mgs.data = #origin_acoustics_level mgs.data
scoreboard players add #attenuation_acoustics mgs.data 1

# Reduce the sound level by 1 when the original sound level (0-4) is greater than the listener's acoustics level
# When in an enclosed space, distant sounds are perceived as closer due to acoustic properties
execute if score #origin_acoustics_level mgs.data matches 0..4 if score #origin_acoustics_level mgs.data > @s mgs.acoustics_level run scoreboard players remove #processed_acoustics mgs.data 1

# Increase the sound level by 1 when the original sound level is less than the listener's acoustics level
# This makes sounds appear louder when the listener is in a more acoustically reflective environment
execute if score #origin_acoustics_level mgs.data < @s mgs.acoustics_level run scoreboard players add #processed_acoustics mgs.data 1

# If (original sound level + 1) is less than listener's acoustics level, increase the sound level by 1
# This creates a smoother sound transition between different acoustic environments
execute if score #attenuation_acoustics mgs.data < @s mgs.acoustics_level run scoreboard players add #processed_acoustics mgs.data 1

# If listener's acoustics level is 5 (water), force the sound level to water regardless of other conditions
execute if score @s mgs.acoustics_level matches 5 run scoreboard players set #processed_acoustics mgs.data 5

# Play the appropriate sound effect based on the calculated sound level
execute if score #processed_acoustics mgs.data matches 0 run function mgs:v5.0.0/sound/hearing/0_distant with storage mgs:gun all.sounds
execute if score #processed_acoustics mgs.data matches 1 run function mgs:v5.0.0/sound/hearing/1_far with storage mgs:gun all.sounds
execute if score #processed_acoustics mgs.data matches 2 run function mgs:v5.0.0/sound/hearing/2_midrange with storage mgs:gun all.sounds
execute if score #processed_acoustics mgs.data matches 3 run function mgs:v5.0.0/sound/hearing/3_near with storage mgs:gun all.sounds
execute if score #processed_acoustics mgs.data matches 4 run function mgs:v5.0.0/sound/hearing/4_closest with storage mgs:gun all.sounds
execute if score #processed_acoustics mgs.data matches 5 run function mgs:v5.0.0/sound/hearing/5_water with storage mgs:gun all.sounds

