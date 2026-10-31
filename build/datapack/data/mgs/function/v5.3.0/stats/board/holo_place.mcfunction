
#> mgs:v5.3.0/stats/board/holo_place
#
# @within	mgs:v5.3.0/stats/board/holo_setup with storage mgs:temp _lb_h
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#

$scoreboard players set #lbx mgs.data $(x)
$scoreboard players set #lby mgs.data $(y)
$scoreboard players set #lbz mgs.data $(z)
execute store result storage mgs:temp _lb_h.x int 1 run scoreboard players operation #lbx mgs.data += #gm_base_x mgs.data
execute store result storage mgs:temp _lb_h.y int 1 run scoreboard players operation #lby mgs.data += #gm_base_y mgs.data
execute store result storage mgs:temp _lb_h.z int 1 run scoreboard players operation #lbz mgs.data += #gm_base_z mgs.data
data modify storage mgs:temp _lb_h.kind set from storage mgs:temp _lb_h.board
function mgs:v5.3.0/stats/board/holo_path with storage mgs:temp _lb_h

