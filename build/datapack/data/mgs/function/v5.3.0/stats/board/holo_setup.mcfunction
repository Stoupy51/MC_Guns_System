
#> mgs:v5.3.0/stats/board/holo_setup
#
# @within	mgs:v5.3.0/zombies/preload_complete
#			mgs:v5.3.0/stats/board/holo_setup
#

data modify storage mgs:temp _lb_h set from storage mgs:temp _lb_iter[0]
execute unless data storage mgs:temp _lb_h.map_id run data modify storage mgs:temp _lb_h.map_id set value ""
execute if data storage mgs:temp _lb_h{map_id:""} run data modify storage mgs:temp _lb_h.map_id set from storage mgs:zombies game.map_id
execute store result storage mgs:temp _lb_h.x int 1 run data get storage mgs:temp _lb_h.pos[0]
execute store result storage mgs:temp _lb_h.y int 1 run data get storage mgs:temp _lb_h.pos[1]
execute store result storage mgs:temp _lb_h.z int 1 run data get storage mgs:temp _lb_h.pos[2]
function mgs:v5.3.0/stats/board/holo_place with storage mgs:temp _lb_h

data remove storage mgs:temp _lb_iter[0]
execute if data storage mgs:temp _lb_iter[0] run function mgs:v5.3.0/stats/board/holo_setup

