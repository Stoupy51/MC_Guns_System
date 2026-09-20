
#> mgs:v5.1.0/zombies/perks/dying_wish_to_1
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/perks/dying_wish_end
#

execute store result storage mgs:temp _dw_dmg.amount double 0.001 run scoreboard players get #dw_hp mgs.data
data modify storage mgs:temp _dw_dmg.type set value "minecraft:generic_kill"
function mgs:v5.1.0/zombies/traps/apply_trap_damage with storage mgs:temp _dw_dmg

