
#> mgs:v5.4.2/zombies/pap/pap_chat_lore_line
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/pap/pap_chat_lore_iter with storage mgs:temp _pap_lore_line
#
# @args		line (unknown)
#

$tellraw @s [{"text":"- ","color":"gray"},$(line)]

