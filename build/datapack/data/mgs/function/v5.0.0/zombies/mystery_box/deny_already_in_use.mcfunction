
#> mgs:v5.0.0/zombies/mystery_box/deny_already_in_use
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.0.0/zombies/mystery_box/on_right_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.mystery_box_is_already_in_use","color":"red"}]
function mgs:v5.0.0/zombies/feedback/sound_deny

