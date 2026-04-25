
#> mgs:v5.0.0/zombies/pap/camo_pick_advance
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/randomize_camo
#			mgs:v5.0.0/zombies/pap/camo_pick_advance
#

data remove storage mgs:temp _pap_camos[0]
scoreboard players add #pap_camo_i mgs.data 1
data modify storage mgs:temp _pap_camo_pick set from storage mgs:temp _pap_camos[0]
execute if score #pap_camo_i mgs.data < #pap_camo_idx mgs.data run function mgs:v5.0.0/zombies/pap/camo_pick_advance

