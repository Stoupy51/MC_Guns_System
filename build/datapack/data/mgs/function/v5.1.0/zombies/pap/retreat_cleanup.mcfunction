
#> mgs:v5.1.0/zombies/pap/retreat_cleanup
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/pap/anim/retreat_finish with storage mgs:temp _pap_retreat
#
# @args		id (unknown)
#

$data modify storage mgs:temp _pap_retreat.slot set from storage mgs:zombies pap_anim_slot."$(id)"

execute as @a[scores={mgs.zb.pap_s=1..}] if score @s mgs.zb.pap_mid = #pap_mid mgs.data run function mgs:v5.1.0/zombies/pap/retreat_clear_owner

$data remove storage mgs:zombies pap_anim_slot."$(id)"

