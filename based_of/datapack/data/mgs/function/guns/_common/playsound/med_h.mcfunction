scoreboard players operation v1 V = v0 V
scoreboard players operation v2 V = v0 V
scoreboard players add v2 V 1
execute if score v0 V matches ..4 if score v0 V > @s acoustics_level run scoreboard players remove v1 V 1
execute if score v0 V < @s acoustics_level run scoreboard players add v1 V 1
execute if score v2 V < @s acoustics_level run scoreboard players add v1 V 1
execute if score @s acoustics_level matches 5 run scoreboard players set v1 V 5
execute if score v1 V matches 0 run function mgs:guns/_common/playsound/med_crack_0
execute if score v1 V matches 1 run function mgs:guns/_common/playsound/med_crack_1
execute if score v1 V matches 2 run function mgs:guns/_common/playsound/med_crack_2
execute if score v1 V matches 3 run function mgs:guns/_common/playsound/med_crack_3
execute if score v1 V matches 4 run function mgs:guns/_common/playsound/med_crack_4
execute if score v1 V matches 5 run function mgs:guns/_common/playsound/med_crack_w
