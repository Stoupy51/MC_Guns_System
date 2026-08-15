
#> mgs:v5.1.0/zombies/perks/apply/mule_kick
#
# @within	???
#

execute at @s run playsound mgs:zombies/perks/mule_kick ambient @s ~ ~ ~ 1.0 1.0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"🎒 ",{"translate":"mgs.mule_kick_third_weapon_slot_unlocked","color":"gold"},[" ",{"text":"+5 XP","color":"gold"}]]
function mgs:v5.1.0/progression/zb/award_perk

