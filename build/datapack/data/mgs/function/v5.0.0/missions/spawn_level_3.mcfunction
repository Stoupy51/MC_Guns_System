
#> mgs:v5.0.0/missions/spawn_level_3
#
# @within	mgs:v5.0.0/missions/spawn_level
#

# Copy enemy positions for iteration
data modify storage mgs:temp _enemy_iter set from storage mgs:missions game.map.enemies.level_3

# Copy enemy config for this level
data modify storage mgs:temp _enemy_config set from storage mgs:missions game.map.enemy_config.level_3

# Iterate and spawn
execute if data storage mgs:temp _enemy_iter[0] run function mgs:v5.0.0/missions/spawn_enemy_iter

