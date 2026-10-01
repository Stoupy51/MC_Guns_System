
#> mgs:v5.1.0/progression/adv/mi/completed/check
#
# @executed	as @a
#
# @within	mgs:v5.1.0/progression/adv/catch_up
#			mgs:v5.1.0/missions/victory [ as @a[scores={mgs.mi.in_game=1}] ]
#

execute if score @s mgs.adv.mi.completed matches 1.. run advancement grant @s only mgs:challenges/mi/completed_1
execute if score @s mgs.adv.mi.completed matches 3.. run advancement grant @s only mgs:challenges/mi/completed_2
execute if score @s mgs.adv.mi.completed matches 5.. run advancement grant @s only mgs:challenges/mi/completed_3
execute if score @s mgs.adv.mi.completed matches 10.. run advancement grant @s only mgs:challenges/mi/completed_4
execute if score @s mgs.adv.mi.completed matches 20.. run advancement grant @s only mgs:challenges/mi/completed_5
execute if score @s mgs.adv.mi.completed matches 35.. run advancement grant @s only mgs:challenges/mi/completed_6
execute if score @s mgs.adv.mi.completed matches 50.. run advancement grant @s only mgs:challenges/mi/completed_7
execute if score @s mgs.adv.mi.completed matches 75.. run advancement grant @s only mgs:challenges/mi/completed_8
execute if score @s mgs.adv.mi.completed matches 100.. run advancement grant @s only mgs:challenges/mi/completed_9
execute if score @s mgs.adv.mi.completed matches 150.. run advancement grant @s only mgs:challenges/mi/completed_10

