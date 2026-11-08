
#> mgs:v5.4.1/zombies/powerups/queue_extract
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/powerups/queue_draw with storage mgs:temp _pu_q
#
# @args		idx (unknown)
#

$execute store result score #pu_spawn_type mgs.data run data get storage mgs:data _pu_queue[$(idx)]
$data remove storage mgs:data _pu_queue[$(idx)]

