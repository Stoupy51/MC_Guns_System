
#> mgs:v5.0.1/zombies/mystery_box/deny_not_your_result
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.0.1/zombies/mystery_box/box_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.wait_for_the_current_player_to_collect_their_result","color":"red"}]
function mgs:v5.0.1/zombies/feedback/sound_deny

