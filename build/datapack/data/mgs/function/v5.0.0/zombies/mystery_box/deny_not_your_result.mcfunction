
#> mgs:v5.0.0/zombies/mystery_box/deny_not_your_result
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.0.0/zombies/mystery_box/on_right_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.wait_for_the_current_player_to_collect_their_result","color":"red"}]
function mgs:v5.0.0/zombies/feedback/sound_deny

