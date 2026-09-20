
#> mgs:v5.1.0/zombies/perks/apply/electric_cherry
#
# @within	???
#

scoreboard players set @s mgs.special.electric_cherry 1
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"🍒 ",{"translate":"mgs.electric_cherry_reloads_discharge_a_shock","color":"blue"},[" ",{"text":"+5 XP","color":"gold"}]]
function mgs:v5.1.0/progression/zb/award_perk

