
#> mgs:v5.3.0/maps/editor/form/box_start
#
# @within	mgs:v5.3.0/maps/editor/form/spawn_apply
#

tag @s add mgs.cs_abox
data remove storage mgs:temp coord_stick.abox
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.right_click_a_corner_of_the_box_with_the_coord_stick_then_the_op","fallback":"Right-click a corner of the box with the Coord Stick, then the opposite corner.","color":"yellow"}]

