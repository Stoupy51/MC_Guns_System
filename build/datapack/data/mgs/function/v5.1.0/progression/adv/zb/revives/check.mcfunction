
#> mgs:v5.1.0/progression/adv/zb/revives/check
#
# @executed	as @a[tag=mgs.xp_earner]
#
# @within	mgs:v5.1.0/progression/zb/award_revive
#			mgs:v5.1.0/progression/adv/catch_up
#

execute if score @s mgs.adv.zb.revives matches 1.. run advancement grant @s only mgs:challenges/zb/revives_1
execute if score @s mgs.adv.zb.revives matches 3.. run advancement grant @s only mgs:challenges/zb/revives_2
execute if score @s mgs.adv.zb.revives matches 5.. run advancement grant @s only mgs:challenges/zb/revives_3
execute if score @s mgs.adv.zb.revives matches 10.. run advancement grant @s only mgs:challenges/zb/revives_4
execute if score @s mgs.adv.zb.revives matches 20.. run advancement grant @s only mgs:challenges/zb/revives_5
execute if score @s mgs.adv.zb.revives matches 35.. run advancement grant @s only mgs:challenges/zb/revives_6
execute if score @s mgs.adv.zb.revives matches 50.. run advancement grant @s only mgs:challenges/zb/revives_7
execute if score @s mgs.adv.zb.revives matches 75.. run advancement grant @s only mgs:challenges/zb/revives_8
execute if score @s mgs.adv.zb.revives matches 100.. run advancement grant @s only mgs:challenges/zb/revives_9
execute if score @s mgs.adv.zb.revives matches 150.. run advancement grant @s only mgs:challenges/zb/revives_10

