
#> mgs:v5.0.0/zombies/wallbuys/count_guns
#
# @within	???
#

scoreboard players set #wb_gun_count mgs.data 0
execute if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true}}] run scoreboard players add #wb_gun_count mgs.data 1
execute if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true}}] run scoreboard players add #wb_gun_count mgs.data 1
execute if items entity @s hotbar.3 *[custom_data~{mgs:{gun:true}}] run scoreboard players add #wb_gun_count mgs.data 1

