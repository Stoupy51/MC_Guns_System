
#> mgs:v5.4.1/zombies/perks/apply/double_tap
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/perks/apply
#

scoreboard players set @s mgs.special.double_tap 1
execute at @s run playsound mgs:zombies/perks/double_tap ambient @s ~ ~ ~ 1.0 1.0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],"🔥 ",{"translate":"mgs.double_tap_more_damage","fallback":"Double Tap! More damage","color":"gold"},[" ",{"text":"+5 XP","color":"gold"}]]
function mgs:v5.4.1/progression/zb/award_perk

