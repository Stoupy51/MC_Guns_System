
#> mgs:v5.1.0/progression/adv/zb/best_round/check
#
# @executed	as @a[scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.1.0/zombies/adv/on_round_end [ as @a[scores={mgs.zb.in_game=1}] ]
#			mgs:v5.1.0/progression/adv/catch_up
#

execute if score @s mgs.adv.zb.best_round matches 5.. run advancement grant @s only mgs:challenges/zb/best_round_1
execute if score @s mgs.adv.zb.best_round matches 10.. run advancement grant @s only mgs:challenges/zb/best_round_2
execute if score @s mgs.adv.zb.best_round matches 15.. run advancement grant @s only mgs:challenges/zb/best_round_3
execute if score @s mgs.adv.zb.best_round matches 20.. run advancement grant @s only mgs:challenges/zb/best_round_4
execute if score @s mgs.adv.zb.best_round matches 25.. run advancement grant @s only mgs:challenges/zb/best_round_5
execute if score @s mgs.adv.zb.best_round matches 30.. run advancement grant @s only mgs:challenges/zb/best_round_6
execute if score @s mgs.adv.zb.best_round matches 35.. run advancement grant @s only mgs:challenges/zb/best_round_7
execute if score @s mgs.adv.zb.best_round matches 40.. run advancement grant @s only mgs:challenges/zb/best_round_8
execute if score @s mgs.adv.zb.best_round matches 50.. run advancement grant @s only mgs:challenges/zb/best_round_9
execute if score @s mgs.adv.zb.best_round matches 60.. run advancement grant @s only mgs:challenges/zb/best_round_10

