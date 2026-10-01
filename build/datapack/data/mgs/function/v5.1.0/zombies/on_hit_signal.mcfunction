
#> mgs:v5.1.0/zombies/on_hit_signal
#
# @within	#mgs:signals/damage
#

execute unless data storage mgs:zombies game{state:"active"} run return fail
execute unless entity @s[tag=mgs.zombie_round] run return fail

# Only player kills drop power-ups.
scoreboard players operation @s mgs.zb.player_hit = #total_tick mgs.data

scoreboard players operation @n[tag=mgs.ticking] mgs.zb.points += #zb_points_hit mgs.config

execute if score @n[tag=mgs.ticking] mgs.special.double_points matches 1.. run scoreboard players operation @n[tag=mgs.ticking] mgs.zb.points += #zb_points_hit mgs.config

