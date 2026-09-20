
#> mgs:v5.1.0/zombies/barricades/on_repair_complete_player
#
# @executed	as @a[tag=mgs.barricade_repairing]
#
# @within	mgs:v5.1.0/zombies/barricades/repair [ as @a[tag=mgs.barricade_repairing] ]
#

# @s = repairing player
tag @s remove mgs.barricade_repairing

# Reward +10 points (max 25 barricade repairs rewarded per round)
execute unless score @s mgs.zb.barricade_repairs matches 25.. run scoreboard players add @s mgs.zb.points 10
execute unless score @s mgs.zb.barricade_repairs matches 25.. run scoreboard players add @s mgs.zb.barricade_repairs 1

data modify storage smithed.actionbar:input message set value {json:[[{"text":"✔ ","color":"green"}, {"translate":"mgs.barricade_repaired"}],{"text":"+10","color":"gold"},[{"text":" ","color":"yellow"}, {"translate":"mgs.points_2"}],[" ",{"text":"+1 XP","color":"gold"}]],priority:"notification",freeze:20}
function mgs:v5.1.0/progression/zb/award_barricade
function #smithed.actionbar:message

