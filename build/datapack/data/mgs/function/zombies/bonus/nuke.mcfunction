
#> mgs:zombies/bonus/nuke
#
# @within	???
#

# Remove any existing nuke activator (in case of concurrent nukes)
tag @a[tag=mgs.nuke_activator] remove mgs.nuke_activator

# Tag activating player for damage attribution
tag @s add mgs.nuke_activator

# Tag all nukable entities as nuked
execute as @e[tag=mgs.nukable] run tag @s add mgs.nuked

# Zero attack damage on all nuked entities (multiply base by 0)
execute as @e[tag=mgs.nuked] run attribute @s minecraft:attack_damage modifier add mgs:nuke_zero_damage -1 add_multiplied_base

# Start kill loop (1 entity per tick)
function mgs:v5.0.0/zombies/bonus/nuke_loop

