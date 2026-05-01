
#> mgs:v5.0.0/zombies/powerups/intercept_item
#
# @within	#common_signals:signals/on_new_item
#

# Only handle items tagged as powerups
execute unless data entity @s Item.components."minecraft:custom_data".mgs.powerup run return 0

# Store type string and integer spawn coordinates in temp storage
data modify storage mgs:temp _pu_spawn.type set from entity @s Item.components."minecraft:custom_data".mgs.powerup.type
execute store result storage mgs:temp _pu_spawn.x int 1 run data get entity @s Pos[0]
execute store result storage mgs:temp _pu_spawn.y int 1 run data get entity @s Pos[1]
execute store result storage mgs:temp _pu_spawn.z int 1 run data get entity @s Pos[2]

# Remove the raw item entity (replaced by visual displays below)
kill @s

# Spawn the visual item_display + text_display at the stored position
function mgs:v5.0.0/zombies/powerups/spawn_display with storage mgs:temp _pu_spawn

