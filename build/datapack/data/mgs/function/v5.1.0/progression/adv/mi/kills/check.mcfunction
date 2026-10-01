
#> mgs:v5.1.0/progression/adv/mi/kills/check
#
# @executed	as @a
#
# @within	mgs:v5.1.0/progression/adv/catch_up
#			mgs:v5.1.0/missions/victory [ as @a[scores={mgs.mi.in_game=1}] ]
#

execute if score @s mgs.adv.mi.kills matches 100.. run advancement grant @s only mgs:challenges/mi/kills_1
execute if score @s mgs.adv.mi.kills matches 250.. run advancement grant @s only mgs:challenges/mi/kills_2
execute if score @s mgs.adv.mi.kills matches 500.. run advancement grant @s only mgs:challenges/mi/kills_3
execute if score @s mgs.adv.mi.kills matches 1000.. run advancement grant @s only mgs:challenges/mi/kills_4
execute if score @s mgs.adv.mi.kills matches 2000.. run advancement grant @s only mgs:challenges/mi/kills_5
execute if score @s mgs.adv.mi.kills matches 3500.. run advancement grant @s only mgs:challenges/mi/kills_6
execute if score @s mgs.adv.mi.kills matches 6000.. run advancement grant @s only mgs:challenges/mi/kills_7
execute if score @s mgs.adv.mi.kills matches 10000.. run advancement grant @s only mgs:challenges/mi/kills_8
execute if score @s mgs.adv.mi.kills matches 20000.. run advancement grant @s only mgs:challenges/mi/kills_9
execute if score @s mgs.adv.mi.kills matches 35000.. run advancement grant @s only mgs:challenges/mi/kills_10

