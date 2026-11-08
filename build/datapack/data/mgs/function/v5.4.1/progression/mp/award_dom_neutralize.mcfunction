
#> mgs:v5.4.1/progression/mp/award_dom_neutralize
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/gamemodes/dom/capture_red [ as @a[tag=mgs.dom_capturer] ]
#			mgs:v5.4.1/multiplayer/gamemodes/dom/capture_blue [ as @a[tag=mgs.dom_capturer] ]
#

# Domination zone dragged back to neutral, the halfway state
scoreboard players add @s mgs.mp.xp_total 5
scoreboard players add @s mgs.mp.xp_prog 5
scoreboard players add @s mgs.mp.xp_session 5
function mgs:v5.4.1/progression/mp/settle

