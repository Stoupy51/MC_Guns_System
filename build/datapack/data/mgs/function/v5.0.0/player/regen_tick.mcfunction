
#> mgs:v5.0.0/player/regen_tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/tick
#

# @s = any player during an active game
execute store result score #hp_cur mgs.data run data get entity @s Health 1
execute if score #hp_cur mgs.data < @s mgs.hp_prev run scoreboard players set @s mgs.last_hit 0
execute unless score #hp_cur mgs.data < @s mgs.hp_prev run scoreboard players add @s mgs.last_hit 1
scoreboard players operation @s mgs.hp_prev = #hp_cur mgs.data
execute unless score @s mgs.last_hit matches 100.. run return 0
execute store result score #hp_max mgs.data run attribute @s minecraft:max_health get 1
execute if score #hp_cur mgs.data >= #hp_max mgs.data run effect clear @s minecraft:regeneration
execute unless score #hp_cur mgs.data >= #hp_max mgs.data run effect give @s minecraft:regeneration 3 2 true

