
#> mgs:v5.1.0/progression/mp/award_kill
#
# @within	mgs:v5.1.0/multiplayer/xp/on_kill
#

# Any kill, every gamemode, via the on_kill signal
scoreboard players add @s mgs.mp.xp_total 10
scoreboard players add @s mgs.mp.xp_prog 10
scoreboard players add @s mgs.mp.xp_session 10
function mgs:v5.1.0/progression/mp/settle

