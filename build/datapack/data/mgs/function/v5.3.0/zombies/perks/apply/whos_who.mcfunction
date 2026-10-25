
#> mgs:v5.3.0/zombies/perks/apply/whos_who
#
# @executed	as @p[tag=mgs.pu_collecting]
#
# @within	mgs:v5.3.0/zombies/perks/apply
#

execute at @s run playsound mgs:zombies/perks/whos_who ambient @s ~ ~ ~ 1.0 1.0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],"👥 ",{"translate":"mgs.whos_who_play_on_as_a_doppelganger_when_downed","fallback":"Who's Who! Play on as a doppelganger when downed","color":"aqua"},[" ",{"text":"+5 XP","color":"gold"}]]
function mgs:v5.3.0/progression/zb/award_perk

