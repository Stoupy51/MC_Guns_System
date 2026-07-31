
#> mgs:v5.1.0/multiplayer/xp/on_kill
#
# @within	#mgs:signals/on_kill
#

execute unless data storage mgs:multiplayer game{state:"active"} run return fail
execute unless score @s mgs.mp.in_game matches 1 run return fail

function mgs:v5.1.0/progression/mp/award_kill
execute if score #mp_kill_headshot mgs.data matches 1 run function mgs:v5.1.0/progression/mp/award_headshot

