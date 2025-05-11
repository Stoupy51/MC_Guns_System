tag @s add self
scoreboard players operation v0 V = @s acoustics_level
execute if score v0 V matches 0 run playsound mgs:common.medlarge_crack_0 player @s ~ ~ ~ 1.0
execute if score v0 V matches 1 run playsound mgs:common.medlarge_crack_1 player @s ~ ~ ~ 1.0
execute if score v0 V matches 2 run playsound mgs:common.medlarge_crack_2 player @s ~ ~ ~ 1.0
execute if score v0 V matches 3 run playsound mgs:common.medlarge_crack_3 player @s ~ ~ ~ 1.0
execute if score v0 V matches 4 run playsound mgs:common.medlarge_crack_4 player @s ~ ~ ~ 1.0
execute if score v0 V matches 5 run playsound mgs:common.medlarge_crack_w player @s ~ ~ ~ 1.0
execute as @a[tag=!self,distance=..240] run function mgs:guns/_common/playsound/medlarge_h
tag @s remove self
