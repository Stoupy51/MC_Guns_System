
#> mgs:v5.0.0/zombies/pap/anim/collect_lookup
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/pap/anim/collect_at_machine with storage mgs:temp _pap_c
#
# @args		id (unknown)
#

$data modify storage mgs:temp _pap_cg.slot set from storage mgs:zombies pap_anim_slot."$(id)"
$data modify storage mgs:temp _pap_cg.id set value $(id)
function mgs:v5.0.0/zombies/pap/anim/collect_give with storage mgs:temp _pap_cg

