
#> mgs:v5.0.0/zombies/barriers/on_repair_complete_player
#
# @executed	as @a[tag=mgs.barrier_repairing]
#
# @within	mgs:v5.0.0/zombies/barriers/repair [ as @a[tag=mgs.barrier_repairing] ]
#

# @s = repairing player
tag @s remove mgs.barrier_repairing
data modify storage smithed.actionbar:input message set value {json:[[{"text":"✔ ","color":"green"}, {"translate":"mgs.barrier_repaired"}]],priority:"notification",freeze:20}
function #smithed.actionbar:message

