
#> mgs:v5.1.0/zombies/pap/on_free_pap
#
# @executed	as @p[tag=mgs.pu_collecting]
#
# @within	mgs:v5.1.0/zombies/powerups/activate/free_pap [ as @p[tag=mgs.pu_collecting] ]
#

# Guard: game must be active
execute unless data storage mgs:zombies game{state:"active"} run return fail
function mgs:v5.1.0/zombies/pap/upgrade_core

