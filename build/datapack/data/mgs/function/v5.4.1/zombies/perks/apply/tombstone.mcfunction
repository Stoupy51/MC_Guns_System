
#> mgs:v5.4.1/zombies/perks/apply/tombstone
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/perks/apply
#

execute at @s run playsound mgs:zombies/perks/tombstone ambient @s ~ ~ ~ 1.0 1.0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],"🪦 ",{"translate":"mgs.tombstone_recover_your_gear_if_you_bleed_out","fallback":"Tombstone! Recover your gear if you bleed out","color":"yellow"},[" ",{"text":"+5 XP","color":"gold"}]]
function mgs:v5.4.1/progression/zb/award_perk

