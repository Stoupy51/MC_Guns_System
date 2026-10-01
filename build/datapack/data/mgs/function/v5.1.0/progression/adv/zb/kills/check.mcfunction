
#> mgs:v5.1.0/progression/adv/zb/kills/check
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/progression/zb/award_kill
#			mgs:v5.1.0/progression/adv/catch_up
#

execute if score @s mgs.adv.zb.kills matches 100.. run advancement grant @s only mgs:challenges/zb/kills_1
execute if score @s mgs.adv.zb.kills matches 250.. run advancement grant @s only mgs:challenges/zb/kills_2
execute if score @s mgs.adv.zb.kills matches 500.. run advancement grant @s only mgs:challenges/zb/kills_3
execute if score @s mgs.adv.zb.kills matches 1000.. run advancement grant @s only mgs:challenges/zb/kills_4
execute if score @s mgs.adv.zb.kills matches 2500.. run advancement grant @s only mgs:challenges/zb/kills_5
execute if score @s mgs.adv.zb.kills matches 5000.. run advancement grant @s only mgs:challenges/zb/kills_6
execute if score @s mgs.adv.zb.kills matches 10000.. run advancement grant @s only mgs:challenges/zb/kills_7
execute if score @s mgs.adv.zb.kills matches 20000.. run advancement grant @s only mgs:challenges/zb/kills_8
execute if score @s mgs.adv.zb.kills matches 35000.. run advancement grant @s only mgs:challenges/zb/kills_9
execute if score @s mgs.adv.zb.kills matches 50000.. run advancement grant @s only mgs:challenges/zb/kills_10

