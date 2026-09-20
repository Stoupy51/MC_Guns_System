
#> mgs:v5.1.0/zombies/perks/apply/quick_revive
#
# @within	???
#

tag @s add mgs.perk.quick_revive
execute at @s run playsound mgs:zombies/perks/quick_revive ambient @s ~ ~ ~ 1.0 1.0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"💚 ",{"translate":"mgs.quick_revive_you_can_revive_teammates","color":"aqua"},[" ",{"text":"+5 XP","color":"gold"}]]
function mgs:v5.1.0/progression/zb/award_perk

