
#> mgs:v5.0.0/zombies/barriers/on_remover_valid
#
# @executed	as @e[tag=mgs.barrier_display] & at @s
#
# @within	mgs:v5.0.0/zombies/barriers/handle_removing
#

# @s = removing zombie, at zombie position (via at @s in handle_removing selector)
scoreboard players set #barrier_remover_valid mgs.data 1
particle minecraft:large_smoke ~ ~1 ~ 0.3 0.3 0.3 0.02 1

