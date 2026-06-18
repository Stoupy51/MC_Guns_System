
#> mgs:v5.0.1/zombies/revive/show_reviver_bar_normal
#
# @executed	at @s
#
# @within	mgs:v5.0.1/zombies/revive/show_reviver_bar
#

data modify storage smithed.actionbar:input message set value {json:[{"translate":"mgs.reviving","color":"yellow"},{"score":{"name":"#rv_reviver_disp","objective":"mgs.data"},"color":"green"},{"text":"/60t","color":"gray"}],priority:"override",freeze:2}
function #smithed.actionbar:message

