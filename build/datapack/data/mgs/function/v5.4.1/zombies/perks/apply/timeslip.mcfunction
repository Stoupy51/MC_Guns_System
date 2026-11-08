
#> mgs:v5.4.1/zombies/perks/apply/timeslip
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/perks/apply
#

scoreboard players set @s mgs.special.timeslip 1

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],"⏳ ",{"translate":"mgs.timeslip_faster_traps_mystery_box","fallback":"Timeslip! Faster traps & Mystery Box","color":"light_purple"},[" ",{"text":"+5 XP","color":"gold"}]]
function mgs:v5.4.1/progression/zb/award_perk

