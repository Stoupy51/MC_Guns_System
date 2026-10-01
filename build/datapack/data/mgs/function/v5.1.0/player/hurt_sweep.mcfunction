
#> mgs:v5.1.0/player/hurt_sweep
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/hurt_tick
#

# @s = a player whose scores say no overlay is applied
scoreboard players set #hurt_was mgs.data 0
execute store success score #hurt_stray mgs.data run posteffect remove @s mgs:hurt_0_1
execute if score #hurt_stray mgs.data matches 1 unless score #hurt_was mgs.data matches 1.. run scoreboard players set #hurt_was mgs.data 1
execute store success score #hurt_stray mgs.data run posteffect remove @s mgs:hurt_0_2
execute if score #hurt_stray mgs.data matches 1 unless score #hurt_was mgs.data matches 2.. run scoreboard players set #hurt_was mgs.data 2
execute store success score #hurt_stray mgs.data run posteffect remove @s mgs:hurt_1_0
execute store success score #hurt_stray mgs.data run posteffect remove @s mgs:hurt_1_1
execute if score #hurt_stray mgs.data matches 1 unless score #hurt_was mgs.data matches 1.. run scoreboard players set #hurt_was mgs.data 1
execute store success score #hurt_stray mgs.data run posteffect remove @s mgs:hurt_1_2
execute if score #hurt_stray mgs.data matches 1 unless score #hurt_was mgs.data matches 2.. run scoreboard players set #hurt_was mgs.data 2
execute store success score #hurt_stray mgs.data run posteffect remove @s mgs:hurt_2_0
execute store success score #hurt_stray mgs.data run posteffect remove @s mgs:hurt_2_1
execute if score #hurt_stray mgs.data matches 1 unless score #hurt_was mgs.data matches 1.. run scoreboard players set #hurt_was mgs.data 1
execute store success score #hurt_stray mgs.data run posteffect remove @s mgs:hurt_2_2
execute if score #hurt_stray mgs.data matches 1 unless score #hurt_was mgs.data matches 2.. run scoreboard players set #hurt_was mgs.data 2
execute if score #hurt_was mgs.data matches 1.. run function mgs:v5.1.0/player/hurt_fade_out

