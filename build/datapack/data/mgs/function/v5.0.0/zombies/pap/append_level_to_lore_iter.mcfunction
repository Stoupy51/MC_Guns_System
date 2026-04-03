
#> mgs:v5.0.0/zombies/pap/append_level_to_lore_iter
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/append_level_to_lore
#			mgs:v5.0.0/zombies/pap/append_level_to_lore_iter
#

execute unless data storage mgs:temp _pap_lore.in[0] run return 0
data modify storage mgs:temp _pap_lore.line set from storage mgs:temp _pap_lore.in[0]
function mgs:v5.0.0/zombies/pap/append_level_to_lore_line with storage mgs:temp _pap_lore
data modify storage mgs:temp _pap_lore.out append from storage mgs:temp _pap_lore.line
data remove storage mgs:temp _pap_lore.in[0]
function mgs:v5.0.0/zombies/pap/append_level_to_lore_iter

