
#> mgs:v5.0.0/zombies/pap/pap_chat_lore_iter
#
# @within	mgs:v5.0.0/zombies/pap/pap_chat_lore_loop with storage mgs:temp _pap_lore_idx
#
# @args		index (unknown)
#

$data modify storage mgs:temp _pap_lore_line.line set from storage mgs:temp _pap_extract.lore[$(index)]
execute if data storage mgs:temp _pap_lore_line.line unless data storage mgs:temp _pap_lore_line.line{text:""} run function mgs:v5.0.0/zombies/pap/pap_chat_lore_line with storage mgs:temp _pap_lore_line

