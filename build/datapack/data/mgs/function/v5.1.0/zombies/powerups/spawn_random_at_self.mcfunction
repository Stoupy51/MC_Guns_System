
#> mgs:v5.1.0/zombies/powerups/spawn_random_at_self
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/powerups/check_drop
#

# Draw next type from the shuffle bag (no repeats until the current cycle is exhausted)
function mgs:v5.1.0/zombies/powerups/queue_draw

# Spawn visuals at @s's position
scoreboard players add #pu_uid mgs.data 1
data modify storage mgs:temp _pu_spawn set value {x:0,y:0,z:0,uid:0}
data modify storage mgs:temp _pu_spawn.x set from entity @s Pos[0]
data modify storage mgs:temp _pu_spawn.y set from entity @s Pos[1]
data modify storage mgs:temp _pu_spawn.z set from entity @s Pos[2]
execute store result storage mgs:temp _pu_spawn.uid int 1 run scoreboard players get #pu_uid mgs.data
function mgs:v5.1.0/zombies/powerups/do_spawn_random

