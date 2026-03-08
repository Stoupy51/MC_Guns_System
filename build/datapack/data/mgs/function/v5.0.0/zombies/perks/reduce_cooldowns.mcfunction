
#> mgs:v5.0.0/zombies/perks/reduce_cooldowns
#
# @within	mgs:v5.0.0/zombies/start_round
#

execute as @a[scores={mgs.zb.in_game=1,mgs.zb.ability_cd=1..}] run scoreboard players remove @s mgs.zb.ability_cd 1

