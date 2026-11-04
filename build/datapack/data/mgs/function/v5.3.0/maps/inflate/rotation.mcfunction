
#> mgs:v5.3.0/maps/inflate/rotation
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/maps/inflate/zombie_spawn_fields
#			mgs:v5.3.0/maps/inflate/player_spawn_zb_fields
#			mgs:v5.3.0/maps/inflate/special_spawn_fields
#			mgs:v5.3.0/maps/inflate/wallbuy_fields
#			mgs:v5.3.0/maps/inflate/door_fields
#			mgs:v5.3.0/maps/inflate/trap_fields
#			mgs:v5.3.0/maps/inflate/perk_machine_fields
#			mgs:v5.3.0/maps/inflate/wunderfizz_fields
#			mgs:v5.3.0/maps/inflate/pap_machine_fields
#			mgs:v5.3.0/maps/inflate/mystery_box_pos_fields
#			mgs:v5.3.0/maps/inflate/power_switch_fields
#			mgs:v5.3.0/maps/inflate/barricade_fields
#

execute if data storage mgs:temp _inf.rotation run return 0
data modify storage mgs:temp _inf.rotation set value [0.0f,0.0f]
execute store result storage mgs:temp _inf.rotation[0] float 1 run data get storage mgs:temp _inf.yaw
execute if data storage mgs:temp _inf.pitch run data modify storage mgs:temp _inf.rotation[1] set from storage mgs:temp _inf.pitch
data remove storage mgs:temp _inf.yaw

