
#> mgs:v5.3.0/zombies/perks/apply/electric_cherry
#
# @executed	as @p[tag=mgs.pu_collecting]
#
# @within	mgs:v5.3.0/zombies/perks/apply
#

scoreboard players set @s mgs.special.electric_cherry 1

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],"🍒 ",{"translate":"mgs.electric_cherry_reloads_discharge_a_shock","fallback":"Electric Cherry! Reloads discharge a shock","color":"blue"},[" ",{"text":"+5 XP","color":"gold"}]]
function mgs:v5.3.0/progression/zb/award_perk

