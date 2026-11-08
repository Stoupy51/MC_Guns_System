
#> mgs:v5.4.1/zombies/revive/show_reviver_bar_quick
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/revive/show_reviver_bar
#

data modify storage smithed.actionbar:input message set value {json:[{"text":"⚡ ","color":"white"},{"translate":"mgs.reviving","fallback":"Reviving... ","color":"aqua"},{"score":{"name":"#rv_rev_sec","objective":"mgs.data"},"color":"green"},{"text":".","color":"green"},{"score":{"name":"#rv_rev_tenth","objective":"mgs.data"},"color":"green"},{"translate":"mgs.s_1_5s","fallback":"s / 1.5s","color":"gray"}],priority:"override",freeze:2}
function #smithed.actionbar:message

