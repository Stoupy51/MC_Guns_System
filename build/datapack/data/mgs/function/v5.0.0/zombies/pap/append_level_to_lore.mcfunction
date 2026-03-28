
#> mgs:v5.0.0/zombies/pap/append_level_to_lore
#
# @within	mgs:v5.0.0/zombies/pap/on_right_click
#

data modify storage mgs:temp _pap_lore.in set from storage mgs:temp _pap_extract.lore
data modify storage mgs:temp _pap_lore.out set value []
execute store result storage mgs:temp _pap_lore.level int 1 run scoreboard players get #pap_next mgs.data
function mgs:v5.0.0/zombies/pap/append_level_to_lore_iter
data modify storage mgs:temp _pap_extract.lore set from storage mgs:temp _pap_lore.out

