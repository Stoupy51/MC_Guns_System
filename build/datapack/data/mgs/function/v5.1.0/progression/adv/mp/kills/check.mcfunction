
#> mgs:v5.1.0/progression/adv/mp/kills/check
#
# @within	mgs:v5.1.0/progression/mp/award_kill
#			mgs:v5.1.0/progression/adv/catch_up
#

execute if score @s mgs.adv.mp.kills matches 25.. run advancement grant @s only mgs:challenges/mp/kills_1
execute if score @s mgs.adv.mp.kills matches 50.. run advancement grant @s only mgs:challenges/mp/kills_2
execute if score @s mgs.adv.mp.kills matches 100.. run advancement grant @s only mgs:challenges/mp/kills_3
execute if score @s mgs.adv.mp.kills matches 250.. run advancement grant @s only mgs:challenges/mp/kills_4
execute if score @s mgs.adv.mp.kills matches 500.. run advancement grant @s only mgs:challenges/mp/kills_5
execute if score @s mgs.adv.mp.kills matches 1000.. run advancement grant @s only mgs:challenges/mp/kills_6
execute if score @s mgs.adv.mp.kills matches 2000.. run advancement grant @s only mgs:challenges/mp/kills_7
execute if score @s mgs.adv.mp.kills matches 3500.. run advancement grant @s only mgs:challenges/mp/kills_8
execute if score @s mgs.adv.mp.kills matches 6000.. run advancement grant @s only mgs:challenges/mp/kills_9
execute if score @s mgs.adv.mp.kills matches 10000.. run advancement grant @s only mgs:challenges/mp/kills_10

