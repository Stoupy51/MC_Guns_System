execute as @e[type=minecraft:marker,tag=wm] if score @s timestamp = v1 V run tag @s add dead
execute store result score v2 V run kill @e[type=minecraft:marker,tag=wm,tag=dead]
scoreboard players operation v0 V -= v2 V
tellraw @a [{"text":"Cleaning Age: ","color":"yellow"},{"score":{"name":"v1","objective":"V"},"color":"yellow"},{"text":" Count: ","color":"yellow"},{"score":{"name":"v2","objective":"V"},"color":"yellow"},{"text":" Remaining: ","color":"yellow"},{"score":{"name":"v0","objective":"V"},"color":"yellow"}]
scoreboard players remove v1 V 1
execute if score v0 V > max_guns S if score v1 V > inactive_sessions S run function mgs:core/init/cleanup_h 