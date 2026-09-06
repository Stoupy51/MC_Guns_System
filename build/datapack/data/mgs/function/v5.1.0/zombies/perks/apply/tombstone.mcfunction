
#> mgs:v5.1.0/zombies/perks/apply/tombstone
#
# @within	???
#

execute at @s run playsound mgs:zombies/perks/tombstone ambient @s ~ ~ ~ 1.0 1.0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"🪦 ",{"translate":"mgs.tombstone_recover_your_gear_if_you_bleed_out","color":"yellow"},[" ",{"text":"+5 XP","color":"gold"}]]
function mgs:v5.1.0/progression/zb/award_perk

## sourceMappingURL=tombstone.mcfunction.map
