
#> mgs:v5.1.0/maps/editor/displays/summon_barrier
#
# @executed	align xyz & positioned ~.5 ~.5 ~.5
#
# @within	mgs:v5.1.0/maps/editor/displays/barrier with storage mgs:temp _ed_bar [ align xyz & positioned ~.5 ~.5 ~.5 ]
#
# @args		yaw (unknown)
#			block (unknown)
#

# Same placement and transform as zombies/barriers/place_at
$summon minecraft:block_display ~ ~ ~ {Rotation:[$(yaw),0f],block_state:$(block),transformation:{left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],translation:[-0.5f,-0.5f,-0.5f],right_rotation:[0f,0f,0f,1f]},Tags:["mgs.editor_display"]}

