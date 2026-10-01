
#> mgs:v5.1.0/progression/adv/mp/level/check
#
# @executed	as @a
#
# @within	#mgs:progression/on_level_up
#			mgs:v5.1.0/progression/adv/catch_up
#

execute if score @s mgs.mp.xp_level matches 10.. run advancement grant @s only mgs:challenges/mp/level_1
execute if score @s mgs.mp.xp_level matches 20.. run advancement grant @s only mgs:challenges/mp/level_2
execute if score @s mgs.mp.xp_level matches 30.. run advancement grant @s only mgs:challenges/mp/level_3
execute if score @s mgs.mp.xp_level matches 40.. run advancement grant @s only mgs:challenges/mp/level_4
execute if score @s mgs.mp.xp_level matches 50.. run advancement grant @s only mgs:challenges/mp/level_5
execute if score @s mgs.mp.xp_level matches 75.. run advancement grant @s only mgs:challenges/mp/level_6
execute if score @s mgs.mp.xp_level matches 100.. run advancement grant @s only mgs:challenges/mp/level_7
execute if score @s mgs.mp.xp_level matches 125.. run advancement grant @s only mgs:challenges/mp/level_8
execute if score @s mgs.mp.xp_level matches 150.. run advancement grant @s only mgs:challenges/mp/level_9
execute if score @s mgs.mp.xp_level matches 200.. run advancement grant @s only mgs:challenges/mp/level_10

