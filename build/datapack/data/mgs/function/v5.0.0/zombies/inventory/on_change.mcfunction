
#> mgs:v5.0.0/zombies/inventory/on_change
#
# @executed	as the player & at current position
#
# @within	advancement mgs:v5.0.0/zombies/inventory_changed
#

advancement revoke @s only mgs:v5.0.0/zombies/inventory_changed
execute unless score @s mgs.zb.in_game matches 1 run return fail
execute if data storage mgs:zombies game{state:"lobby"} run return fail
execute if data storage mgs:zombies game{state:"ended"} run return fail

# Prevent recursive re-entry (item replace in swap/enforce can re-trigger inventory_changed)
execute if entity @s[tag=mgs.inv_checking] run return fail
tag @s add mgs.inv_checking
function mgs:v5.0.0/zombies/inventory/check_slots
tag @s remove mgs.inv_checking

