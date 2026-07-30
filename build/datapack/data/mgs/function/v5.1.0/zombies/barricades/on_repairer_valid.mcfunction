
#> mgs:v5.1.0/zombies/barricades/on_repairer_valid
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/barricades/handle_repair
#

# @s = repairing player
scoreboard players set #barricade_repair_valid mgs.data 1
# Actionbar progress: show remaining ticks out of 30
data modify storage smithed.actionbar:input message set value {json:[[{"text":"🔧 ","color":"aqua"}, {"translate":"mgs.repairing_barricade"}],{"score":{"name":"#barricade_rp_cur","objective":"mgs.data"},"color":"yellow"},{"text":"/30","color":"gray"}],priority:"conditional",freeze:2}
function #smithed.actionbar:message

