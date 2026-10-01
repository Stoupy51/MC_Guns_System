
#> mgs:v5.1.0/progression/adv/mp/wins/check
#
# @executed	as @a[scores={mgs.mp.in_game=1},tag=mgs.xp_winner]
#
# @within	mgs:v5.1.0/progression/mp/award_match_win
#			mgs:v5.1.0/progression/adv/catch_up
#

execute if score @s mgs.adv.mp.wins matches 1.. run advancement grant @s only mgs:challenges/mp/wins_1
execute if score @s mgs.adv.mp.wins matches 3.. run advancement grant @s only mgs:challenges/mp/wins_2
execute if score @s mgs.adv.mp.wins matches 5.. run advancement grant @s only mgs:challenges/mp/wins_3
execute if score @s mgs.adv.mp.wins matches 10.. run advancement grant @s only mgs:challenges/mp/wins_4
execute if score @s mgs.adv.mp.wins matches 20.. run advancement grant @s only mgs:challenges/mp/wins_5
execute if score @s mgs.adv.mp.wins matches 35.. run advancement grant @s only mgs:challenges/mp/wins_6
execute if score @s mgs.adv.mp.wins matches 50.. run advancement grant @s only mgs:challenges/mp/wins_7
execute if score @s mgs.adv.mp.wins matches 75.. run advancement grant @s only mgs:challenges/mp/wins_8
execute if score @s mgs.adv.mp.wins matches 100.. run advancement grant @s only mgs:challenges/mp/wins_9
execute if score @s mgs.adv.mp.wins matches 150.. run advancement grant @s only mgs:challenges/mp/wins_10

