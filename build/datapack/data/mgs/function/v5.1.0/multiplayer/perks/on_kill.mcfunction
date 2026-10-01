
#> mgs:v5.1.0/multiplayer/perks/on_kill
#
# @within	#mgs:signals/on_kill
#

execute unless score @s mgs.mp.in_game matches 1 run return fail

# Scavenger refills the spare magazines on every kill, not the loaded weapon.
execute if score @s mgs.special.scavenger matches 1 run function mgs:v5.1.0/multiplayer/perks/scavenger_refill

# Quick Fix starts health regen at once (last_hit threshold 100).
execute if score @s mgs.special.quick_fix matches 1 run scoreboard players set @s mgs.last_hit 100
execute if score @s mgs.special.quick_fix matches 1 run effect give @s minecraft:regeneration 3 1 true

