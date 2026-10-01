
#> mgs:v5.1.0/progression/adv/zb/box/check
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/progression/zb/award_mystery_box
#			mgs:v5.1.0/progression/adv/catch_up
#

execute if score @s mgs.adv.zb.box matches 1.. run advancement grant @s only mgs:challenges/zb/box_1
execute if score @s mgs.adv.zb.box matches 5.. run advancement grant @s only mgs:challenges/zb/box_2
execute if score @s mgs.adv.zb.box matches 10.. run advancement grant @s only mgs:challenges/zb/box_3
execute if score @s mgs.adv.zb.box matches 25.. run advancement grant @s only mgs:challenges/zb/box_4
execute if score @s mgs.adv.zb.box matches 50.. run advancement grant @s only mgs:challenges/zb/box_5
execute if score @s mgs.adv.zb.box matches 75.. run advancement grant @s only mgs:challenges/zb/box_6
execute if score @s mgs.adv.zb.box matches 100.. run advancement grant @s only mgs:challenges/zb/box_7
execute if score @s mgs.adv.zb.box matches 200.. run advancement grant @s only mgs:challenges/zb/box_8
execute if score @s mgs.adv.zb.box matches 300.. run advancement grant @s only mgs:challenges/zb/box_9
execute if score @s mgs.adv.zb.box matches 500.. run advancement grant @s only mgs:challenges/zb/box_10

