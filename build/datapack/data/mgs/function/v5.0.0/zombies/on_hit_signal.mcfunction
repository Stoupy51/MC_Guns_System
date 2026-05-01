
#> mgs:v5.0.0/zombies/on_hit_signal
#
# @within	#mgs:signals/damage
#

# Only process if zombies game is active & If the hit target is a live round zombie
execute unless data storage mgs:zombies game{state:"active"} run return fail
execute unless entity @s[tag=mgs.zombie_round] run return fail

# Award +10 bullet hit points to the shooter
scoreboard players operation @n[tag=mgs.ticking] mgs.zb.points += #zb_points_hit mgs.config

# Refresh sidebar
function mgs:v5.0.0/zombies/refresh_sidebar

# Double points bonus for bullet hit points
execute if score @n[tag=mgs.ticking] mgs.special.double_points matches 1.. run scoreboard players operation @n[tag=mgs.ticking] mgs.zb.points += #zb_points_hit mgs.config

