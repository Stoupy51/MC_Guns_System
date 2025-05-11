tag @a remove ini
execute if entity @e[type=minecraft:marker,tag=wm,scores={timestamp=0}] as @e[type=minecraft:marker,tag=wm] if score @s timestamp < max_sessions S run scoreboard players add @s timestamp 1
scoreboard players set v0 V 0
scoreboard players operation v1 V = max_sessions S
execute as @e[type=minecraft:marker,tag=wm] run scoreboard players add v0 V 1
execute if score v0 V > max_guns S run tellraw @a [{"text":"Too many guns in the world! Cleaning old guns! ","color":"yellow"},{"score":{"name":"v0","objective":"V"},"color":"yellow"},{"text":"/","color":"yellow"},{"score":{"name":"max_guns","objective":"S"},"color":"yellow"}]
execute if score v0 V > max_guns S run function mgs:core/init/cleanup_h
kill @e[tag=fired]
kill @e[type=minecraft:marker,tag=lp]