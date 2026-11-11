
#> mgs:v5.4.2/zombies/pap/on_free_pap
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/powerups/activate/free_pap [ as @p[tag=mgs.pu_collecting] ]
#

execute unless data storage mgs:zombies game{state:"active"} run return fail
function mgs:v5.4.2/zombies/pap/upgrade_core

