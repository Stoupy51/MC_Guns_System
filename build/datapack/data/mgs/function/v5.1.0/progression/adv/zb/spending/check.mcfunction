
#> mgs:v5.1.0/progression/adv/zb/spending/check
#
# @executed	as @a[scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.1.0/progression/zb/award_points_spent
#			mgs:v5.1.0/progression/adv/catch_up
#

execute if score @s mgs.adv.zb.spending matches 100.. run advancement grant @s only mgs:challenges/zb/spending_1
execute if score @s mgs.adv.zb.spending matches 250.. run advancement grant @s only mgs:challenges/zb/spending_2
execute if score @s mgs.adv.zb.spending matches 500.. run advancement grant @s only mgs:challenges/zb/spending_3
execute if score @s mgs.adv.zb.spending matches 1000.. run advancement grant @s only mgs:challenges/zb/spending_4
execute if score @s mgs.adv.zb.spending matches 2000.. run advancement grant @s only mgs:challenges/zb/spending_5
execute if score @s mgs.adv.zb.spending matches 3500.. run advancement grant @s only mgs:challenges/zb/spending_6
execute if score @s mgs.adv.zb.spending matches 6000.. run advancement grant @s only mgs:challenges/zb/spending_7
execute if score @s mgs.adv.zb.spending matches 10000.. run advancement grant @s only mgs:challenges/zb/spending_8
execute if score @s mgs.adv.zb.spending matches 20000.. run advancement grant @s only mgs:challenges/zb/spending_9
execute if score @s mgs.adv.zb.spending matches 35000.. run advancement grant @s only mgs:challenges/zb/spending_10

