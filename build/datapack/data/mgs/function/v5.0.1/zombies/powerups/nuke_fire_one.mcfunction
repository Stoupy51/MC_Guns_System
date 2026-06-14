
#> mgs:v5.0.1/zombies/powerups/nuke_fire_one
#
# @executed	as @e[tag=mgs.nukable] & at @s
#
# @within	mgs:v5.0.1/zombies/powerups/activate/nuke [ as @e[tag=mgs.nukable] & at @s ]
#

data merge entity @s {Fire:1200s}
effect give @s minecraft:fire_resistance infinite 0 true
particle minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.02 12 force @a[scores={mgs.zb.in_game=1},distance=..48]
particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.5 0.3 0.02 6 force @a[scores={mgs.zb.in_game=1},distance=..48]

