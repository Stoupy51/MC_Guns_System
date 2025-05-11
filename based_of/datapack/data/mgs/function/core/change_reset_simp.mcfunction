scoreboard players set @s fire 0
scoreboard players set @s selector 0
tag @s[scores={cooldown=1..}] remove reloading
tag @s[tag=loaded] remove loaded
scoreboard players set @s cooldown 0
execute if score @s weapon matches 1.. run tag @s add switch
stopsound @s voice