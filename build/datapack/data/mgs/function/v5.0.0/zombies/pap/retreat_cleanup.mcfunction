
#> mgs:v5.0.0/zombies/pap/retreat_cleanup
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/pap/anim_retreat_finish with storage mgs:temp _pap_retreat
#
# @args		id (unknown)
#

# Get the stored slot for this machine
$data modify storage mgs:temp _pap_retreat.slot set from storage mgs:zombies pap_anim_slot."$(id)"

# Find owner by matching PAP machine ID and clear their orphaned magazine
execute as @a[scores={mgs.zb.pap_s=1..}] if score @s mgs.zb.pap_mid = #pap_mid mgs.data run function mgs:v5.0.0/zombies/pap/retreat_clear_owner

# Clean stored slot data
$data remove storage mgs:zombies pap_anim_slot."$(id)"

