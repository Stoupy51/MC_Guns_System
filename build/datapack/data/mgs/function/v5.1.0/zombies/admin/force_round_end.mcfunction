
#> mgs:v5.1.0/zombies/admin/force_round_end
#
# @within	mgs:v5.1.0/zombies/admin/round_skip_1
#			mgs:v5.1.0/zombies/admin/round_skip_5
#			mgs:v5.1.0/zombies/admin/round_skip_10
#			mgs:v5.1.0/zombies/admin/round_skip_50
#

kill @e[tag=mgs.zombie_round]
scoreboard players set #zb_to_spawn mgs.data 0

