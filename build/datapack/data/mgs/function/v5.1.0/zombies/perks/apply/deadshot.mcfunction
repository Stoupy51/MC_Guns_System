
#> mgs:v5.1.0/zombies/perks/apply/deadshot
#
# @within	???
#

scoreboard players set @s mgs.special.deadshot 1
execute at @s run playsound mgs:zombies/perks/deadshot ambient @s ~ ~ ~ 1.0 1.0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"🎯 ",{"translate":"mgs.deadshot_daiquiri_accuracy_recoil","color":"dark_green"},[" ",{"text":"+5 XP","color":"gold"}]]
function mgs:v5.1.0/progression/zb/award_perk

