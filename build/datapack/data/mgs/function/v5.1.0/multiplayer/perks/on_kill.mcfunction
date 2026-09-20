
#> mgs:v5.1.0/multiplayer/perks/on_kill
#
# @within	#mgs:signals/on_kill
#

# Only relevant for players in an active multiplayer game
execute unless score @s mgs.mp.in_game matches 1 run return fail

# Scavenger: refill the player's spare magazines on every kill (the loaded weapon is
# left untouched, so they still have to reload — they just never run dry on reserve)
execute if score @s mgs.special.scavenger matches 1 run function mgs:v5.1.0/multiplayer/perks/scavenger_refill

# Quick Fix: kick off health regen immediately (last_hit threshold is 100)
execute if score @s mgs.special.quick_fix matches 1 run scoreboard players set @s mgs.last_hit 100
execute if score @s mgs.special.quick_fix matches 1 run effect give @s minecraft:regeneration 3 1 true

