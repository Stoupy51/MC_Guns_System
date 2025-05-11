execute store result score v0 V run data get entity @s SelectedItem.tag.WUID
scoreboard players set v1 V 0
execute as @e[type=minecraft:marker,tag=wm] if score @s UID = v0 V run scoreboard players set v1 V 1
execute if score v1 V matches 1 run scoreboard players operation @s weapon_id = v0 V