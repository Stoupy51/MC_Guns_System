
#> mgs:v5.0.0/zombies/pap/pap_chat_lore_loop
#
# @within	mgs:v5.0.0/zombies/pap/pap_chat_lore_loop
#			mgs:v5.0.0/zombies/pap/pap_chat_message
#

execute store result storage mgs:temp _pap_lore_idx.index int 1 run scoreboard players get #pap_li mgs.data
function mgs:v5.0.0/zombies/pap/pap_chat_lore_iter with storage mgs:temp _pap_lore_idx
scoreboard players add #pap_li mgs.data 1
execute if score #pap_li mgs.data < #pap_lore_len mgs.data run function mgs:v5.0.0/zombies/pap/pap_chat_lore_loop

