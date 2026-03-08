
#> mgs:v5.0.0/zombies/inventory/on_change
#
# @executed	as the player & at current position
#
# @within	advancement mgs:v5.0.0/zombies/inventory_changed
#

# Only process during active zombies game
execute unless score @s mgs.zb.in_game matches 1 run return fail
execute if data storage mgs:zombies game{state:"lobby"} run return fail
execute if data storage mgs:zombies game{state:"ended"} run return fail

# Revoke advancement to re-detect
advancement revoke @s only mgs:v5.0.0/zombies/inventory_changed

# Check & fix slot integrity
function mgs:v5.0.0/zombies/inventory/check_slots

