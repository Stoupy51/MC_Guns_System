
#> mgs:v5.4.1/zombies/perks/reduce_cooldowns
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/start_round
#

execute as @a[scores={mgs.zb.in_game=1,mgs.zb.ability_cd=1..}] run scoreboard players remove @s mgs.zb.ability_cd 1

