
#> mgs:v5.0.0/zombies/pap/check_scope_variants
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/repap_scope_only with storage mgs:temp _pap_scope_bw
#
# @args		base_weapon (unknown)
#

scoreboard players set #pap_has_scopes mgs.data 0
$execute if data storage mgs:zombies scope_variants."$(base_weapon)"[1] run scoreboard players set #pap_has_scopes mgs.data 1

