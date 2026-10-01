
#> mgs:v5.1.0/zombies/hurt_player/on_hurt
#
# @executed	as the player & at current position
#
# @within	advancement mgs:v5.1.0/zombies/hurt_player
#

# Revoked first, so it can trigger again.
advancement revoke @s only mgs:v5.1.0/zombies/hurt_player
execute unless data storage mgs:zombies game{state:"active"} run return fail
execute unless score @s mgs.zb.in_game matches 1.. run return fail

# Counters the small upward knockback.
function mgs:v5.1.0/zombies/hurt_player/launch_downward

# Budgeted per player (see vocals). `unless` rather than a return: the passives below run on every hit.
execute unless score @s mgs.zb.vox_attack > #total_tick mgs.data run function mgs:v5.1.0/zombies/vocals/attack

execute if score @s mgs.special.widows_wine matches 1 run function mgs:v5.1.0/zombies/perks/widows_on_hurt

