
#> mgs:v5.0.0/zombies/mystery_box/deny_pool_empty
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.0.0/zombies/mystery_box/pick_random_result
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.mystery_box_pool_is_empty","color":"red"}]
function mgs:v5.0.0/zombies/feedback/sound_deny

