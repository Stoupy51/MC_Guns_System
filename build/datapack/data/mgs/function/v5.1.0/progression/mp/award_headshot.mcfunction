
#> mgs:v5.1.0/progression/mp/award_headshot
#
# @within	mgs:v5.1.0/multiplayer/xp/on_kill
#

# Added ON TOP of kill, so a headshot kill is worth double
scoreboard players add @s mgs.mp.xp_total 10
scoreboard players add @s mgs.mp.xp_prog 10
scoreboard players add @s mgs.mp.xp_session 10
function mgs:v5.1.0/progression/mp/settle

