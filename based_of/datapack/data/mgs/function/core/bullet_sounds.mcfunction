scoreboard players set v14 V 0
execute if block ~ ~ ~ #mgs:sounds/special_sound run scoreboard players set v14 V 1
execute if score v15 V matches 2 if score v14 V matches 0 run playsound mgs:common.soft_bullet_impact block @a ~ ~ ~ 1
execute if score v15 V matches 3.. if score v14 V matches 0 run playsound mgs:common.solid_bullet_impact block @a ~ ~ ~ 1
execute if score v14 V matches 1 run function mgs:core/bullet_sounds_special