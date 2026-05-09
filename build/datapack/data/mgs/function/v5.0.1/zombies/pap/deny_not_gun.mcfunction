
#> mgs:v5.0.1/zombies/pap/deny_not_gun
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.1/zombies/pap/on_right_click
#			mgs:v5.0.1/zombies/pap/upgrade_core
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.selected_slot_does_not_contain_a_weapon","color":"red"}]
function mgs:v5.0.1/zombies/feedback/sound_deny

