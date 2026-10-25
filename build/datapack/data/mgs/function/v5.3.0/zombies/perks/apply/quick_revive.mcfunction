
#> mgs:v5.3.0/zombies/perks/apply/quick_revive
#
# @executed	as @p[tag=mgs.pu_collecting]
#
# @within	mgs:v5.3.0/zombies/perks/apply
#

tag @s add mgs.perk.quick_revive
execute at @s run playsound mgs:zombies/perks/quick_revive ambient @s ~ ~ ~ 1.0 1.0
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],"💚 ",{"translate":"mgs.quick_revive_you_can_revive_teammates","fallback":"Quick Revive! You can revive teammates","color":"aqua"},[" ",{"text":"+5 XP","color":"gold"}]]
function mgs:v5.3.0/progression/zb/award_perk

