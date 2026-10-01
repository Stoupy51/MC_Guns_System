
#> mgs:v5.1.0/progression/adv/mp/objectives/check
#
# @executed	as @a[tag=mgs.dom_capturer]
#
# @within	mgs:v5.1.0/progression/mp/award_dom_capture
#			mgs:v5.1.0/progression/mp/award_hp_capture
#			mgs:v5.1.0/progression/mp/award_bomb_plant
#			mgs:v5.1.0/progression/mp/award_bomb_defuse
#			mgs:v5.1.0/progression/mp/award_site_destroyed
#			mgs:v5.1.0/progression/adv/catch_up
#

execute if score @s mgs.adv.mp.objectives matches 5.. run advancement grant @s only mgs:challenges/mp/objectives_1
execute if score @s mgs.adv.mp.objectives matches 10.. run advancement grant @s only mgs:challenges/mp/objectives_2
execute if score @s mgs.adv.mp.objectives matches 25.. run advancement grant @s only mgs:challenges/mp/objectives_3
execute if score @s mgs.adv.mp.objectives matches 50.. run advancement grant @s only mgs:challenges/mp/objectives_4
execute if score @s mgs.adv.mp.objectives matches 100.. run advancement grant @s only mgs:challenges/mp/objectives_5
execute if score @s mgs.adv.mp.objectives matches 200.. run advancement grant @s only mgs:challenges/mp/objectives_6
execute if score @s mgs.adv.mp.objectives matches 350.. run advancement grant @s only mgs:challenges/mp/objectives_7
execute if score @s mgs.adv.mp.objectives matches 600.. run advancement grant @s only mgs:challenges/mp/objectives_8
execute if score @s mgs.adv.mp.objectives matches 1000.. run advancement grant @s only mgs:challenges/mp/objectives_9
execute if score @s mgs.adv.mp.objectives matches 1500.. run advancement grant @s only mgs:challenges/mp/objectives_10

