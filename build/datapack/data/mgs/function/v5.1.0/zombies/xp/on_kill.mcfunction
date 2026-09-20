
#> mgs:v5.1.0/zombies/xp/on_kill
#
# @within	#mgs:signals/on_kill
#

execute unless data storage mgs:zombies game{state:"active"} run return fail
execute unless score @s mgs.zb.in_game matches 1 run return fail
execute unless data storage mgs:signals on_kill{headshot:1} run return fail

function mgs:v5.1.0/progression/zb/award_headshot

