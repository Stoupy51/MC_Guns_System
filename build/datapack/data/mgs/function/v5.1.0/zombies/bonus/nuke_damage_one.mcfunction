
#> mgs:v5.1.0/zombies/bonus/nuke_damage_one
#
# @executed	as @n[tag=mgs.nuked,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/bonus/nuke_loop [ as @n[tag=mgs.nuked,sort=random] & at @s ]
#

tag @s remove mgs.nuked

attribute @s minecraft:attack_damage modifier remove mgs:nuke_zero_damage

# No player attacker, so nuke kills do not pay kill points (the Nuke pays a flat bonus).
damage @s 999999 mgs:bullet

