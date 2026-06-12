
#> mgs:v5.0.1/zombies/mystery_box/deny_pool_empty
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.0.1/zombies/mystery_box/pick_random_result
#

# Clear any stale result so downstream checks treat this pull as failed
data remove storage mgs:zombies mystery_box.result
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.the_mystery_box_has_no_weapons_available","color":"red"}]
function mgs:v5.0.1/zombies/feedback/sound_deny

