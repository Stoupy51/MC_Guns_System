
#> mgs:v5.4.2/zombies/powerups/spawn_random_at_self
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/powerups/check_drop
#

# No repeats until the bag is empty.
function mgs:v5.4.2/zombies/powerups/queue_draw

scoreboard players add #pu_uid mgs.data 1
data modify storage mgs:temp _pu_spawn set value {x:0,y:0,z:0,uid:0}
execute at @s summon minecraft:marker run function mgs:v5.4.2/shared/probe_pos
data modify storage mgs:temp _pu_spawn.x set from storage mgs:temp _probe_pos[0]
data modify storage mgs:temp _pu_spawn.y set from storage mgs:temp _probe_pos[1]
data modify storage mgs:temp _pu_spawn.z set from storage mgs:temp _probe_pos[2]
execute store result storage mgs:temp _pu_spawn.uid int 1 run scoreboard players get #pu_uid mgs.data
function mgs:v5.4.2/zombies/powerups/do_spawn_random

