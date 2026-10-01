
#> mgs:v5.1.0/progression/adv/mp/headshots/check
#
# @within	mgs:v5.1.0/progression/mp/award_headshot
#			mgs:v5.1.0/progression/adv/catch_up
#

execute if score @s mgs.adv.mp.headshots matches 10.. run advancement grant @s only mgs:challenges/mp/headshots_1
execute if score @s mgs.adv.mp.headshots matches 25.. run advancement grant @s only mgs:challenges/mp/headshots_2
execute if score @s mgs.adv.mp.headshots matches 50.. run advancement grant @s only mgs:challenges/mp/headshots_3
execute if score @s mgs.adv.mp.headshots matches 100.. run advancement grant @s only mgs:challenges/mp/headshots_4
execute if score @s mgs.adv.mp.headshots matches 250.. run advancement grant @s only mgs:challenges/mp/headshots_5
execute if score @s mgs.adv.mp.headshots matches 500.. run advancement grant @s only mgs:challenges/mp/headshots_6
execute if score @s mgs.adv.mp.headshots matches 1000.. run advancement grant @s only mgs:challenges/mp/headshots_7
execute if score @s mgs.adv.mp.headshots matches 1750.. run advancement grant @s only mgs:challenges/mp/headshots_8
execute if score @s mgs.adv.mp.headshots matches 3000.. run advancement grant @s only mgs:challenges/mp/headshots_9
execute if score @s mgs.adv.mp.headshots matches 5000.. run advancement grant @s only mgs:challenges/mp/headshots_10

