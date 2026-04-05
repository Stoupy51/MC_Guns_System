
#> mgs:v5.0.0/zombies/pap/annotate_int_delta
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/annotate_lore
#			mgs:v5.0.0/zombies/pap/annotate_pellets_line
#

execute store result storage mgs:temp _pap_ann.index int 1 run scoreboard players get #pap_li mgs.data
data modify storage mgs:temp _pap_ann.suffix set value ""
execute store result storage mgs:temp _pap_ann.value int 1 run scoreboard players get #pap_new mgs.data
function mgs:v5.0.0/zombies/pap/annotate_append_int with storage mgs:temp _pap_ann

