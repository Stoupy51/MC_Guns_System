
#> mgs:v5.4.2/zombies/perks/apply/mule_kick
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/perks/apply
#

execute at @s run playsound mgs:zombies/perks/mule_kick ambient @s ~ ~ ~ 1.0 1.0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],"🎒 ",{"translate":"mgs.mule_kick_third_weapon_slot_unlocked","fallback":"Mule Kick! Third weapon slot unlocked","color":"gold"},[" ",{"text":"+5 XP","color":"gold"}]]
function mgs:v5.4.2/progression/zb/award_perk

