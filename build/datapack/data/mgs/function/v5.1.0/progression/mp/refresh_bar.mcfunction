
#> mgs:v5.1.0/progression/mp/refresh_bar
#
# @executed	as @a
#
# @within	mgs:v5.1.0/progression/mp/init
#			mgs:v5.1.0/progression/mp/settle
#			mgs:v5.1.0/progression/mp/recompute
#			mgs:v5.1.0/progression/tick_player
#

execute unless score @s mgs.mp.xp_level matches 1.. run return 0

scoreboard players operation #xp_req mgs.data = @s mgs.mp.xp_level
scoreboard players operation #xp_req mgs.data *= #10 mgs.data
scoreboard players add #xp_req mgs.data 40
scoreboard players operation #xp_bar mgs.data = @s mgs.mp.xp_prog
scoreboard players operation #xp_bar mgs.data *= #1011 mgs.data
scoreboard players operation #xp_bar mgs.data /= #xp_req mgs.data

execute store result storage mgs:temp _xp.points int 1 run scoreboard players get #xp_bar mgs.data
execute store result storage mgs:temp _xp.level int 1 run scoreboard players get @s mgs.mp.xp_level
function mgs:v5.1.0/progression/apply_bar with storage mgs:temp _xp

