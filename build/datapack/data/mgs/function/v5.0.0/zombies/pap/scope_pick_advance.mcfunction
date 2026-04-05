
#> mgs:v5.0.0/zombies/pap/scope_pick_advance
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/randomize_scope
#			mgs:v5.0.0/zombies/pap/scope_pick_advance
#

data remove storage mgs:temp _pap_scopes[0]
scoreboard players add #pap_scope_i mgs.data 1
data modify storage mgs:temp _pap_scope_pick set from storage mgs:temp _pap_scopes[0]
execute if score #pap_scope_i mgs.data < #pap_scope_idx mgs.data run function mgs:v5.0.0/zombies/pap/scope_pick_advance

