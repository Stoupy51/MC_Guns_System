
#> mgs:v5.0.1/zombies/revive/show_reviver_bar_normal
#
# @executed	at @s
#
# @within	mgs:v5.0.1/zombies/revive/show_reviver_bar
#

data modify storage smithed.actionbar:input message set value {json:[{"translate":"mgs.reviving","color":"yellow"},{"score":{"name":"#rv_rev_sec","objective":"mgs.data"},"color":"green"},{"text":".","color":"green"},{"score":{"name":"#rv_rev_tenth","objective":"mgs.data"},"color":"green"},{"translate":"mgs.s_3_0s","color":"gray"}],priority:"override",freeze:2}
function #smithed.actionbar:message

