
#> mgs:v5.1.0/zombies/powerups/intercept_item
#
# @within	#common_signals:signals/on_new_item
#

execute unless data entity @s Item.components."minecraft:custom_data".mgs.powerup run return 0

scoreboard players add #pu_uid mgs.data 1
data modify storage mgs:temp _pu_spawn.type set from entity @s Item.components."minecraft:custom_data".mgs.powerup.type
execute store result storage mgs:temp _pu_spawn.x int 1 run data get entity @s Pos[0]
execute store result storage mgs:temp _pu_spawn.y int 1 run data get entity @s Pos[1]
execute store result storage mgs:temp _pu_spawn.z int 1 run data get entity @s Pos[2]
execute store result storage mgs:temp _pu_spawn.uid int 1 run scoreboard players get #pu_uid mgs.data

kill @s

function mgs:v5.1.0/zombies/powerups/spawn_display with storage mgs:temp _pu_spawn

