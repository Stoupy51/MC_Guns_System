
# Add self tag to the executing entity to prevent self-targeting in subsequent commands
tag @s add self

# Store the entity's acoustics level in v0 V scoreboard
scoreboard players operation v0 V = @s acoustics_level

# Play different sound effects based on the acoustics level (0-5)
# Each level has its own unique sound effect
execute if score v0 V matches 0 run playsound mgs:common.med_crack_0 player @s ~ ~ ~ 1.0
execute if score v0 V matches 1 run playsound mgs:common.med_crack_1 player @s ~ ~ ~ 1.0
execute if score v0 V matches 2 run playsound mgs:common.med_crack_2 player @s ~ ~ ~ 1.0
execute if score v0 V matches 3 run playsound mgs:common.med_crack_3 player @s ~ ~ ~ 1.0
execute if score v0 V matches 4 run playsound mgs:common.med_crack_4 player @s ~ ~ ~ 1.0
execute if score v0 V matches 5 run playsound mgs:common.med_crack_w player @s ~ ~ ~ 1.0

# Execute med_h function for all players within 224 blocks who don't have the self tag
# This handles sound propagation to nearby players
execute as @a[tag=!self,distance=..224] run function mgs:guns/_common/playsound/med_h

# Remove the self tag after processing is complete
tag @s remove self

