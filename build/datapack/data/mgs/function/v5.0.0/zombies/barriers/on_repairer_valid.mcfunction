
#> mgs:v5.0.0/zombies/barriers/on_repairer_valid
#
# @executed	as @e[tag=mgs.barrier_display] & at @s
#
# @within	mgs:v5.0.0/zombies/barriers/handle_repair
#

# @s = repairing player
scoreboard players set #barrier_repair_valid mgs.data 1
# Actionbar progress: show remaining ticks out of 30
data modify storage smithed.actionbar:input message set value {json:[[{"text":"🔧 ","color":"aqua"}, {"translate":"mgs.repairing_barrier"}],{"score":{"name":"#barrier_rp_cur","objective":"mgs.data"},"color":"yellow"},{"text":"/30","color":"gray"}],priority:"conditional",freeze:2}
function #smithed.actionbar:message

