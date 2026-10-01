
#> mgs:v5.1.0/progression/adv/zb/pack_a_punch/check
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.1.0/progression/zb/award_pack_a_punch
#			mgs:v5.1.0/progression/adv/catch_up
#

execute if score @s mgs.adv.zb.pap matches 1.. run advancement grant @s only mgs:challenges/zb/pack_a_punch_1
execute if score @s mgs.adv.zb.pap matches 3.. run advancement grant @s only mgs:challenges/zb/pack_a_punch_2
execute if score @s mgs.adv.zb.pap matches 5.. run advancement grant @s only mgs:challenges/zb/pack_a_punch_3
execute if score @s mgs.adv.zb.pap matches 10.. run advancement grant @s only mgs:challenges/zb/pack_a_punch_4
execute if score @s mgs.adv.zb.pap matches 20.. run advancement grant @s only mgs:challenges/zb/pack_a_punch_5
execute if score @s mgs.adv.zb.pap matches 35.. run advancement grant @s only mgs:challenges/zb/pack_a_punch_6
execute if score @s mgs.adv.zb.pap matches 50.. run advancement grant @s only mgs:challenges/zb/pack_a_punch_7
execute if score @s mgs.adv.zb.pap matches 75.. run advancement grant @s only mgs:challenges/zb/pack_a_punch_8
execute if score @s mgs.adv.zb.pap matches 100.. run advancement grant @s only mgs:challenges/zb/pack_a_punch_9
execute if score @s mgs.adv.zb.pap matches 150.. run advancement grant @s only mgs:challenges/zb/pack_a_punch_10

