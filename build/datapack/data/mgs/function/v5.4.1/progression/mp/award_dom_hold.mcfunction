
#> mgs:v5.4.1/progression/mp/award_dom_hold
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/gamemodes/dom/score_tick [ at @s ]
#

# Standing in a zone your team owns, once per 5s score tick
scoreboard players add @s mgs.mp.xp_total 1
scoreboard players add @s mgs.mp.xp_prog 1
scoreboard players add @s mgs.mp.xp_session 1
function mgs:v5.4.1/progression/mp/settle

