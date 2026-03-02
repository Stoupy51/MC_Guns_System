
#> mgs:v5.0.0/zombies/bonus/nuke_damage_one
#
# @executed	as @n[tag=mgs.nuked,sort=random] & at @s
#
# @within	mgs:v5.0.0/zombies/bonus/nuke_loop [ as @n[tag=mgs.nuked,sort=random] & at @s ]
#

# Remove nuked tag (entity will no longer be selected in loop)
tag @s remove mgs.nuked

# Remove attack damage modifier (restore normal damage)
attribute @s minecraft:attack_damage modifier remove mgs:nuke_zero_damage

# Deal lethal damage from the nuke activator player
damage @s 999999 mgs:bullet by @n[tag=mgs.nuke_activator]

