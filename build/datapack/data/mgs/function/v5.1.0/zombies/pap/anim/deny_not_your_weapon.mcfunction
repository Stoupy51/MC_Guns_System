
#> mgs:v5.1.0/zombies/pap/anim/deny_not_your_weapon
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.1.0/zombies/pap/anim/collect
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.this_upgraded_weapon_belongs_to_another_player","color":"red"}]
function mgs:v5.1.0/zombies/feedback/sound_deny

