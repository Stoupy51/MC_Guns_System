
#> mgs:v5.3.0/maps/editor/name_to_title
#
# @executed	as @n[tag=mgs.new_zb_marker]
#
# @within	mgs:v5.3.0/maps/editor/summon_zb_object_iter [ as @n[tag=mgs.new_zb_marker] ]
#			mgs:v5.3.0/maps/editor/handle_zb_object [ as @n[tag=mgs.new_zb_marker] ]
#

execute if data entity @s data.name run data modify entity @s data.title set from entity @s data.name
data remove entity @s data.name

