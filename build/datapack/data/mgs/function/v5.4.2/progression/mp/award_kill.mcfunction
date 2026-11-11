
#> mgs:v5.4.2/progression/mp/award_kill
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/xp/on_kill
#

# Any kill, every gamemode, via the on_kill signal
scoreboard players add @s mgs.mp.xp_total 10
scoreboard players add @s mgs.mp.xp_prog 10
scoreboard players add @s mgs.mp.xp_session 10

# Observers of this award
scoreboard players add @s mgs.adv.mp.kills 1
function mgs:v5.4.2/progression/adv/mp/kills/check
function mgs:v5.4.2/progression/mp/settle

