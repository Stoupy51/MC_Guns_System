
#> mgs:v5.1.0/zombies/pap/deny_not_supported
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.1.0/zombies/pap/on_right_click
#			mgs:v5.1.0/zombies/pap/upgrade_core
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.this_weapon_cannot_be_pack_a_punched","color":"red"}]
function mgs:v5.1.0/zombies/feedback/sound_deny

