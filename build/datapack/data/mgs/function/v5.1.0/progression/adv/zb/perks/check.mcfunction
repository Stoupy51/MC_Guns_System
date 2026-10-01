
#> mgs:v5.1.0/progression/adv/zb/perks/check
#
# @within	mgs:v5.1.0/progression/zb/award_perk
#			mgs:v5.1.0/progression/adv/catch_up
#

execute if score @s mgs.adv.zb.perks matches 5.. run advancement grant @s only mgs:challenges/zb/perks_1
execute if score @s mgs.adv.zb.perks matches 10.. run advancement grant @s only mgs:challenges/zb/perks_2
execute if score @s mgs.adv.zb.perks matches 25.. run advancement grant @s only mgs:challenges/zb/perks_3
execute if score @s mgs.adv.zb.perks matches 50.. run advancement grant @s only mgs:challenges/zb/perks_4
execute if score @s mgs.adv.zb.perks matches 75.. run advancement grant @s only mgs:challenges/zb/perks_5
execute if score @s mgs.adv.zb.perks matches 100.. run advancement grant @s only mgs:challenges/zb/perks_6
execute if score @s mgs.adv.zb.perks matches 150.. run advancement grant @s only mgs:challenges/zb/perks_7
execute if score @s mgs.adv.zb.perks matches 200.. run advancement grant @s only mgs:challenges/zb/perks_8
execute if score @s mgs.adv.zb.perks matches 300.. run advancement grant @s only mgs:challenges/zb/perks_9
execute if score @s mgs.adv.zb.perks matches 500.. run advancement grant @s only mgs:challenges/zb/perks_10

