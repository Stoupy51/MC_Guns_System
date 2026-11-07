
#> mgs:v5.4.0/maps/editor/form/box_corner
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/utils/coord_stick_relative
#

execute align xyz run particle firework ~.5 ~.5 ~.5 0.4 0.4 0.4 0.01 100 force @a[distance=..20]
execute summon minecraft:marker run function mgs:v5.4.0/utils/coord_stick_store_pos
execute unless data storage mgs:temp coord_stick.abox run return run function mgs:v5.4.0/maps/editor/form/box_first
function mgs:v5.4.0/maps/editor/form/box_second

