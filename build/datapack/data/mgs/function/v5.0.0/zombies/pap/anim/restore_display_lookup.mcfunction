
#> mgs:v5.0.0/zombies/pap/anim/restore_display_lookup
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/pap/anim/restore_display with storage mgs:temp _pap_restore
#
# @args		id (unknown)
#

$data modify storage mgs:temp _pap_restore_disp.tag set from storage mgs:zombies pap_data."$(id)".display_tag
$data modify storage mgs:temp _pap_restore_disp.item_id set from storage mgs:zombies pap_data."$(id)".display_item_id
$data modify storage mgs:temp _pap_restore_disp.item_model set from storage mgs:zombies pap_data."$(id)".display_item_model
$data modify storage mgs:temp _pap_restore_disp.yaw set from storage mgs:zombies pap_data."$(id)".display_yaw
function mgs:v5.0.0/zombies/display/summon_machine_display with storage mgs:temp _pap_restore_disp

