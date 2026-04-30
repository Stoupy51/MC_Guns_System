
#> mgs:v5.0.0/zombies/on_hit_signal
#
# @within	#mgs:signals/damage
#

# Only process if zombies game is active & If the hit target is a live round zombie
execute unless data storage mgs:zombies game{{state:"active"}} run return fail
execute unless entity @s[tag=mgs.zombie_round] run return fail

# Award +10 bullet hit points to the shooter
scoreboard players operation @n[tag=mgs.ticking] mgs.zb.points += #zb_points_hit mgs.config

