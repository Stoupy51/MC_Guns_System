
#> mgs:v5.1.0/zombies/revive/show_reviver_bar_quick
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/revive/show_reviver_bar
#

data modify storage smithed.actionbar:input message set value {json:[[{"text":"⚡ ","color":"aqua"}, {"translate":"mgs.reviving"}],{"score":{"name":"#rv_rev_sec","objective":"mgs.data"},"color":"green"},{"text":".","color":"green"},{"score":{"name":"#rv_rev_tenth","objective":"mgs.data"},"color":"green"},{"translate":"mgs.s_1_5s","color":"gray"}],priority:"override",freeze:2}
function #smithed.actionbar:message

