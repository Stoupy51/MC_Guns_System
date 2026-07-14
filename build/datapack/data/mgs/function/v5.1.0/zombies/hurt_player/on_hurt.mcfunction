
#> mgs:v5.1.0/zombies/hurt_player/on_hurt
#
# @executed	as the player & at current position
#
# @within	advancement mgs:v5.1.0/zombies/hurt_player
#

# Revoke advancement and stop if the player is not in the zombies game
advancement revoke @s only mgs:v5.1.0/zombies/hurt_player
execute unless data storage mgs:zombies game{state:"active"} run return fail
execute unless score @s mgs.zb.in_game matches 1.. run return fail

# Launch player downward to counter the slight jump boost from knockback.
function mgs:v5.1.0/zombies/hurt_player/launch_downward

