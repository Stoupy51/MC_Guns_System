
#> mgs:v5.1.0/progression/mp/award_dom_capture
#
# @executed	as @a[tag=mgs.dom_capturer]
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/dom/capture_red [ as @a[tag=mgs.dom_capturer] ]
#			mgs:v5.1.0/multiplayer/gamemodes/dom/capture_blue [ as @a[tag=mgs.dom_capturer] ]
#

# Domination zone taken, to every contributor standing on it
scoreboard players add @s mgs.mp.xp_total 20
scoreboard players add @s mgs.mp.xp_prog 20
scoreboard players add @s mgs.mp.xp_session 20
function mgs:v5.1.0/progression/mp/settle

