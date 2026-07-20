
#> mgs:v5.1.0/zombies/wallbuys/deny_knife_owned
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.1.0/zombies/wallbuys/buy_knife
#

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_already_own_this_knife","color":"yellow"}]
function mgs:v5.1.0/zombies/feedback/sound_deny

