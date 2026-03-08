
#> mgs:v5.0.0/zombies/spawn_zombie
#
# @within	mgs:v5.0.0/zombies/spawn_tick
#

# Tag nearby unlocked zombie spawns
# First pass: 32 blocks from any alive player
execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] at @s run tag @e[tag=mgs.spawn_zb,tag=mgs.spawn_unlocked,distance=..32] add mgs.zb_near

# Second pass: 64 blocks if none found
execute unless entity @e[tag=mgs.zb_near] as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] at @s run tag @e[tag=mgs.spawn_zb,tag=mgs.spawn_unlocked,distance=..64] add mgs.zb_near

# Fallback: any unlocked spawn
execute unless entity @e[tag=mgs.zb_near] run tag @e[tag=mgs.spawn_zb,tag=mgs.spawn_unlocked] add mgs.zb_near

# Pick random from tagged set and spawn
execute as @n[tag=mgs.zb_near,sort=random] at @s run function mgs:v5.0.0/zombies/do_spawn_zombie

# Cleanup
tag @e[tag=mgs.zb_near] remove mgs.zb_near

