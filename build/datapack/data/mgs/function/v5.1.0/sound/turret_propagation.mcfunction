
#> mgs:v5.1.0/sound/turret_propagation
#
# @executed	as @a[distance=0.001..224] & facing entity @s eyes
#
# @within	mgs:v5.1.0/sound/turret_fire [ as @a[distance=0.001..224] & facing entity @s eyes ]
#

# Make copies of the original (turret) acoustics level to work on
scoreboard players operation #processed_acoustics mgs.data = #origin_acoustics_level mgs.data
scoreboard players operation #attenuation_acoustics mgs.data = #origin_acoustics_level mgs.data
scoreboard players add #attenuation_acoustics mgs.data 1

# Same acoustics blending as the player propagation, against each listener's own acoustics level
execute if score #origin_acoustics_level mgs.data matches 0..4 if score #origin_acoustics_level mgs.data > @s mgs.acoustics_level run scoreboard players remove #processed_acoustics mgs.data 1
execute if score #origin_acoustics_level mgs.data < @s mgs.acoustics_level run scoreboard players add #processed_acoustics mgs.data 1
execute if score #attenuation_acoustics mgs.data < @s mgs.acoustics_level run scoreboard players add #processed_acoustics mgs.data 1
execute if score @s mgs.acoustics_level matches 5 run scoreboard players set #processed_acoustics mgs.data 5

# Play the appropriate crack variant (reuses the shared hearing/* distance table)
execute if score #processed_acoustics mgs.data matches 0 run function mgs:v5.1.0/sound/hearing/0_distant with storage mgs:temp _turret_snd
execute if score #processed_acoustics mgs.data matches 1 run function mgs:v5.1.0/sound/hearing/1_far with storage mgs:temp _turret_snd
execute if score #processed_acoustics mgs.data matches 2 run function mgs:v5.1.0/sound/hearing/2_midrange with storage mgs:temp _turret_snd
execute if score #processed_acoustics mgs.data matches 3 run function mgs:v5.1.0/sound/hearing/3_near with storage mgs:temp _turret_snd
execute if score #processed_acoustics mgs.data matches 4 run function mgs:v5.1.0/sound/hearing/4_closest with storage mgs:temp _turret_snd
execute if score #processed_acoustics mgs.data matches 5 run function mgs:v5.1.0/sound/hearing/5_water with storage mgs:temp _turret_snd

