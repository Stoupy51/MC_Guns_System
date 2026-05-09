
#> mgs:v5.0.1/zombies/powerups/spawn_random_at_self
#
# @executed	at @s
#
# @within	mgs:v5.0.1/zombies/powerups/check_drop
#

# Draw next type from the shuffle bag (no repeats until all 9 used)
function mgs:v5.0.1/zombies/powerups/queue_draw

# Spawn visuals at @s's position
data modify storage mgs:temp _pu_spawn set value {x:0,y:0,z:0}
data modify storage mgs:temp _pu_spawn.x set from entity @s Pos[0]
data modify storage mgs:temp _pu_spawn.y set from entity @s Pos[1]
data modify storage mgs:temp _pu_spawn.z set from entity @s Pos[2]
function mgs:v5.0.1/zombies/powerups/do_spawn_random with storage mgs:temp _pu_spawn

