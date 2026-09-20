
#> mgs:v5.1.0/progression/zb/award_barricade
#
# @executed	as @a[tag=mgs.barricade_repairing]
#
# @within	mgs:v5.1.0/zombies/barricades/on_repair_complete_player
#

# Repairing a barricade; already capped at 25 repairs per round
scoreboard players add @s mgs.zb.xp_total 1
scoreboard players add @s mgs.zb.xp_prog 1
function mgs:v5.1.0/progression/zb/settle

