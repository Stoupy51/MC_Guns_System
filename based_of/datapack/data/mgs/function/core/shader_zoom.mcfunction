scoreboard players operation v0 V = @s weapon
scoreboard players set v1 V 0
execute if score v0 V matches 19 run scoreboard players set v1 V 1
execute if score v0 V matches 29 run scoreboard players set v1 V 1
execute if score v0 V matches 39 run scoreboard players set v1 V 1
execute if score v0 V matches 49 run scoreboard players set v1 V 1
execute if score v0 V matches 59 run scoreboard players set v1 V 1
execute if score v0 V matches 69 run scoreboard players set v1 V 1
execute if score v0 V matches 79 run scoreboard players set v1 V 1
execute if score v0 V matches 89 run scoreboard players set v1 V 1
execute if score v0 V matches 139 run scoreboard players set v1 V 1
execute if score v0 V matches 219 run scoreboard players set v1 V 1
execute if score v0 V matches 239 run scoreboard players set v1 V 1
execute if score v0 V matches 419 run scoreboard players set v1 V 1
execute if score v0 V matches 429 run scoreboard players set v1 V 1
execute if score v0 V matches 436 run scoreboard players set v1 V 1
execute if score v0 V matches 449 run scoreboard players set v1 V 1
execute if score v0 V matches 529 run scoreboard players set v1 V 1

execute if score v1 V matches 1 if score @s shader_pws matches 1 if score @s shader_delay matches ..-1 run scoreboard players operation @s shader_delay = shaderZoomReapp V
execute if score v1 V matches 1 if score @s shader_pws matches 0 run scoreboard players operation @s shader_delay = shaderZoomDelay V
execute if score v1 V matches 0 if score @s shader_pws matches 1 run scoreboard players operation @s shader_delay = shaderClearReapp V
execute if score v1 V matches 0 if score @s shader_delay = shaderClearReapp V run scoreboard players set @s shader_mode 6
execute if score v1 V matches 0 if score @s shader_delay matches 0 run scoreboard players set @s shader_mode 6
execute if score v1 V matches 1 if score @s shader_delay matches 0 run scoreboard players set @s shader_mode 5
execute if score v1 V matches 1 if score @s shader_delay matches 1 run scoreboard players set @s shader_mode 4

scoreboard players operation @s shader_pws = v1 V