
#> mgs:v5.1.0/progression/mp/award_dom_hold
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/dom/score_tick [ at @s ]
#

# Standing in a zone your team owns, once per 5s score tick
scoreboard players add @s mgs.mp.xp_total 1
scoreboard players add @s mgs.mp.xp_prog 1
scoreboard players add @s mgs.mp.xp_session 1
function mgs:v5.1.0/progression/mp/settle

