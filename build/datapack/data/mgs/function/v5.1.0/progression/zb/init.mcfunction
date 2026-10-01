
#> mgs:v5.1.0/progression/zb/init
#
# @executed	as @a
#
# @within	mgs:v5.1.0/progression/tick_player
#

scoreboard players add @s mgs.zb.xp_total 0
scoreboard players add @s mgs.zb.xp_prog 0
scoreboard players set @s mgs.zb.xp_level 1

# XP with no level: a first run of this system or a retune of awards; the total is the only trustworthy number, so the caches are rebuilt from it.
execute if score @s mgs.zb.xp_total matches 1.. run function mgs:v5.1.0/progression/zb/recompute
function mgs:v5.1.0/progression/zb/refresh_bar

