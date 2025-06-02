
# Copy the original acoustics level (v0 V) to v1 V for processing
scoreboard players operation v1 V = v0 V

# Copy the original acoustics level to v2 V and add 1
# This is used for distance-based sound attenuation
scoreboard players operation v2 V = v0 V
scoreboard players add v2 V 1

# Sound attenuation logic:
# If original sound level is 0-4 and greater than listener's acoustics level,
# reduce the sound level by 1
execute if score v0 V matches ..4 if score v0 V > @s acoustics_level run scoreboard players remove v1 V 1

# If original sound level is less than listener's acoustics level,
# increase the sound level by 1
execute if score v0 V < @s acoustics_level run scoreboard players add v1 V 1

#
execute if score v2 V < @s acoustics_level run scoreboard players add v1 V 1

# If listener's acoustics level is 5, force the sound level to 5
# This ensures maximum sound level for listeners with highest acoustics
execute if score @s acoustics_level matches 5 run scoreboard players set v1 V 5

# Play the appropriate sound effect based on the calculated sound level (v1 V)
# Each level (0-5) has its own unique sound effect
execute if score v1 V matches 0 run function mgs:guns/_common/playsound/med_crack_0
execute if score v1 V matches 1 run function mgs:guns/_common/playsound/med_crack_1
execute if score v1 V matches 2 run function mgs:guns/_common/playsound/med_crack_2
execute if score v1 V matches 3 run function mgs:guns/_common/playsound/med_crack_3
execute if score v1 V matches 4 run function mgs:guns/_common/playsound/med_crack_4
execute if score v1 V matches 5 run function mgs:guns/_common/playsound/med_crack_w
