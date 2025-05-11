execute as @a run function mgs:core/shader_zoom
execute as @a[predicate=mgs:gun,scores={shader_mode=..4}] at @s anchored eyes positioned ^ ^ ^ unless block ~ ~ ~ water unless block ~ ~ ~ lava if score @s shader_pshots < @s shots run function mgs:core/shader_muzzle
execute as @a[scores={shader_mode=1}] at @s anchored eyes run particle minecraft:dust 0.011 0.0 0.0 0.01 ^ ^ ^-500 0 0 0 0 1 force @s
execute as @a[scores={shader_mode=2}] at @s anchored eyes run particle minecraft:dust 0.0 0.011 0.0 0.01 ^ ^ ^-500 0 0 0 0 1 force @s
execute as @a[scores={shader_mode=3}] at @s anchored eyes run particle minecraft:dust 0.0 0.0 0.011 0.01 ^ ^ ^-500 0 0 0 0 1 force @s
execute as @a[scores={shader_mode=4..5}] at @s anchored eyes run particle minecraft:dust 0.011 0.011 0.0 0.01 ^ ^ ^-500 0 0 0 0 1 force @s
execute as @a[scores={shader_mode=6}] at @s anchored eyes run particle minecraft:dust 0.011 0.0 0.011 0.01 ^ ^ ^-500 0 0 0 0 1 force @s
scoreboard players set @a shader_mode 0
scoreboard players remove @a[scores={shader_delay=0..}] shader_delay 2
execute as @a run scoreboard players operation @s shader_pshots = @s shots