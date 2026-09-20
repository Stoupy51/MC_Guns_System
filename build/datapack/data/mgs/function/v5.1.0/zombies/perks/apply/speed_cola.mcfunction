
#> mgs:v5.1.0/zombies/perks/apply/speed_cola
#
# @within	???
#

scoreboard players set @s mgs.special.quick_reload 50
execute at @s run playsound mgs:zombies/perks/speed_cola ambient @s ~ ~ ~ 1.0 1.0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"⚡ ",{"translate":"mgs.speed_cola_faster_reload","color":"green"},[" ",{"text":"+5 XP","color":"gold"}]]
function mgs:v5.1.0/progression/zb/award_perk

