
#> mgs:v5.0.0/zombies/powerups/queue_extract
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/powerups/queue_draw with storage mgs:temp _pu_q
#
# @args		idx (unknown)
#

$execute store result score #pu_spawn_type mgs.data run data get storage mgs:data _pu_queue[$(idx)]
$data remove storage mgs:data _pu_queue[$(idx)]

