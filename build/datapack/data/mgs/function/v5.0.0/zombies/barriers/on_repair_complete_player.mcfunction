
#> mgs:v5.0.0/zombies/barriers/on_repair_complete_player
#
# @executed	as @a[tag=mgs.barrier_repairing]
#
# @within	mgs:v5.0.0/zombies/barriers/repair [ as @a[tag=mgs.barrier_repairing] ]
#

# @s = repairing player
tag @s remove mgs.barrier_repairing

# Reward +10 points (max 25 barrier repairs rewarded per round)
execute unless score @s mgs.zb.barrier_repairs matches 25.. run scoreboard players add @s mgs.zb.points 10
execute unless score @s mgs.zb.barrier_repairs matches 25.. run scoreboard players add @s mgs.zb.barrier_repairs 1

data modify storage smithed.actionbar:input message set value {json:[[{"text":"✔ ","color":"green"}, {"translate":"mgs.barrier_repaired"}],{"text":"+10","color":"gold"},[{"text":" ","color":"yellow"}, {"translate":"mgs.points_2"}]],priority:"notification",freeze:20}
function #smithed.actionbar:message

