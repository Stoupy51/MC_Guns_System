
#> mgs:v5.1.0/progression/zb/award_kill
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/zombies/check_kill_points
#

# Per zombie, any kill type, via the totalKillCount delta
scoreboard players operation @s mgs.zb.xp_total += #xp_gain mgs.data
scoreboard players operation @s mgs.zb.xp_prog += #xp_gain mgs.data
function mgs:v5.1.0/progression/zb/settle

