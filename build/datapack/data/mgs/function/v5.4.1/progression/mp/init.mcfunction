
#> mgs:v5.4.1/progression/mp/init
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/progression/tick_player
#			mgs:v5.4.1/stats/login
#

scoreboard players add @s mgs.mp.xp_total 0
scoreboard players add @s mgs.mp.xp_prog 0
scoreboard players set @s mgs.mp.xp_level 1

# XP with no level: a first run of this system or a retune of awards; the total is the only trustworthy number, so the caches are rebuilt from it.
execute if score @s mgs.mp.xp_total matches 1.. run function mgs:v5.4.1/progression/mp/recompute
function mgs:v5.4.1/progression/mp/refresh_bar

