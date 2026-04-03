
#> mgs:v5.0.0/zombies/perks/deny_already_owned
#
# @executed	as @n[tag=mgs.pk_new]
#
# @within	mgs:v5.0.0/zombies/perks/on_right_click
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_already_own_this_perk","color":"yellow"}]
function mgs:v5.0.0/zombies/feedback/sound_deny

