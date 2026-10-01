
#> mgs:v5.1.0/progression/adv/zb/level/check
#
# @executed	as @a
#
# @within	#mgs:progression/on_level_up
#			mgs:v5.1.0/progression/adv/catch_up
#

execute if score @s mgs.zb.xp_level matches 10.. run advancement grant @s only mgs:challenges/zb/level_1
execute if score @s mgs.zb.xp_level matches 20.. run advancement grant @s only mgs:challenges/zb/level_2
execute if score @s mgs.zb.xp_level matches 30.. run advancement grant @s only mgs:challenges/zb/level_3
execute if score @s mgs.zb.xp_level matches 40.. run advancement grant @s only mgs:challenges/zb/level_4
execute if score @s mgs.zb.xp_level matches 50.. run advancement grant @s only mgs:challenges/zb/level_5
execute if score @s mgs.zb.xp_level matches 75.. run advancement grant @s only mgs:challenges/zb/level_6
execute if score @s mgs.zb.xp_level matches 100.. run advancement grant @s only mgs:challenges/zb/level_7
execute if score @s mgs.zb.xp_level matches 125.. run advancement grant @s only mgs:challenges/zb/level_8
execute if score @s mgs.zb.xp_level matches 150.. run advancement grant @s only mgs:challenges/zb/level_9
execute if score @s mgs.zb.xp_level matches 200.. run advancement grant @s only mgs:challenges/zb/level_10

