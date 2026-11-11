
#> mgs:v5.4.2/maps/editor/displays/summon_power_switch
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/displays/power_switch with storage mgs:temp _ed_ps [ align xyz & positioned ~.5 ~.5 ~.5 ]
#
# @args		yaw (unknown)
#

$summon minecraft:item_display ~ ~ ~ {Rotation:[$(yaw),0f],Tags:["mgs.ed_disp_new"],item_display:"fixed",billboard:"fixed",item:{id:"minecraft:lever",count:1,components:{"minecraft:item_model":"mgs:power_switch"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1f,1f,1f]}}

