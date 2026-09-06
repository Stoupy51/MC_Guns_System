
#> mgs:v5.1.0/missions/xp/on_kill
#
# @within	#mgs:signals/on_kill
#

execute unless data storage mgs:missions game{state:"active"} run return fail
execute unless score @s mgs.mi.in_game matches 1 run return fail

function mgs:v5.1.0/progression/mp/award_mission_kill
execute if data storage mgs:signals on_kill{headshot:1} run function mgs:v5.1.0/progression/mp/award_mission_headshot

## sourceMappingURL=on_kill.mcfunction.map
