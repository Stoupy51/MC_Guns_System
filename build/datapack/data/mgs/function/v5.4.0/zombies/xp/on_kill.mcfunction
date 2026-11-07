
#> mgs:v5.4.0/zombies/xp/on_kill
#
# @within	#mgs:signals/on_kill
#			mgs:v5.4.0/dialog/close_then
#

execute unless data storage mgs:zombies game{state:"active"} run return fail
execute unless score @s mgs.zb.in_game matches 1 run return fail
execute unless data storage mgs:signals on_kill{headshot:1} run return fail

function mgs:v5.4.0/progression/zb/award_headshot

