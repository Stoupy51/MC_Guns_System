
#> mgs:v5.4.2/progression/zb/award_kill
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/check_kill_points
#

# Per zombie, any kill type, via the totalKillCount delta
scoreboard players operation @s mgs.zb.xp_total += #xp_gain mgs.data
scoreboard players operation @s mgs.zb.xp_prog += #xp_gain mgs.data

# Observers of this award
scoreboard players operation @s mgs.adv.zb.kills += #zb_kills_delta mgs.data
function mgs:v5.4.2/progression/adv/zb/kills/check
function mgs:v5.4.2/progression/zb/settle

