scoreboard players operation v0 V = @s weapon
scoreboard players operation v0 V %= 10 C
scoreboard players set @s shader_mode 2
execute if score @s weapon matches 100..299 run scoreboard players set @s shader_mode 3
execute if score v0 V matches 5.. run scoreboard players set @s shader_mode 1