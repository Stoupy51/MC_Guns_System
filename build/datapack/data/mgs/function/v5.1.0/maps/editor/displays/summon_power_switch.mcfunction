
#> mgs:v5.1.0/maps/editor/displays/summon_power_switch
#
# @executed	align xyz & positioned ~.5 ~.5 ~.5
#
# @within	mgs:v5.1.0/maps/editor/displays/power_switch with storage mgs:temp _ed_ps [ align xyz & positioned ~.5 ~.5 ~.5 ]
#
# @args		yaw (unknown)
#

$summon minecraft:item_display ~ ~ ~ {Rotation:[$(yaw),0f],Tags:["mgs.editor_display"],item_display:"fixed",billboard:"fixed",item:{id:"minecraft:lever",count:1,components:{"minecraft:item_model":"mgs:power_switch"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1f,1f,1f]}}

