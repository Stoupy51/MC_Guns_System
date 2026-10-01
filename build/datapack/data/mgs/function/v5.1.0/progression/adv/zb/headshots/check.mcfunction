
#> mgs:v5.1.0/progression/adv/zb/headshots/check
#
# @within	mgs:v5.1.0/progression/zb/award_headshot
#			mgs:v5.1.0/progression/adv/catch_up
#

execute if score @s mgs.adv.zb.headshots matches 50.. run advancement grant @s only mgs:challenges/zb/headshots_1
execute if score @s mgs.adv.zb.headshots matches 100.. run advancement grant @s only mgs:challenges/zb/headshots_2
execute if score @s mgs.adv.zb.headshots matches 250.. run advancement grant @s only mgs:challenges/zb/headshots_3
execute if score @s mgs.adv.zb.headshots matches 500.. run advancement grant @s only mgs:challenges/zb/headshots_4
execute if score @s mgs.adv.zb.headshots matches 1000.. run advancement grant @s only mgs:challenges/zb/headshots_5
execute if score @s mgs.adv.zb.headshots matches 2000.. run advancement grant @s only mgs:challenges/zb/headshots_6
execute if score @s mgs.adv.zb.headshots matches 3500.. run advancement grant @s only mgs:challenges/zb/headshots_7
execute if score @s mgs.adv.zb.headshots matches 6000.. run advancement grant @s only mgs:challenges/zb/headshots_8
execute if score @s mgs.adv.zb.headshots matches 10000.. run advancement grant @s only mgs:challenges/zb/headshots_9
execute if score @s mgs.adv.zb.headshots matches 15000.. run advancement grant @s only mgs:challenges/zb/headshots_10

