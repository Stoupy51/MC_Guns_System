tag @s add self
scoreboard players operation v0 V = @s acoustics_level
execute if score v0 V matches 0 run playsound mgs:common.large_crack_0 player @s ~ ~ ~ 1.0
execute if score v0 V matches 1 run playsound mgs:common.large_crack_1 player @s ~ ~ ~ 1.0
execute if score v0 V matches 2 run playsound mgs:common.large_crack_2 player @s ~ ~ ~ 1.0
execute if score v0 V matches 3 run playsound mgs:common.large_crack_3 player @s ~ ~ ~ 1.0
execute if score v0 V matches 4 run playsound mgs:common.large_crack_4 player @s ~ ~ ~ 1.0
execute if score v0 V matches 5 run playsound mgs:common.large_crack_w player @s ~ ~ ~ 1.0
execute as @a[tag=!self,distance=..256] run function mgs:guns/_common/playsound/large_h
tag @s remove self
