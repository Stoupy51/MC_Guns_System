
#> mgs:v5.4.1/stats/mp/gamemode_win
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/progression/mp/award_match_win with storage mgs:multiplayer game
#
# @args		gamemode (unknown)
#

$scoreboard players add @s mgs.st.mp.$(gamemode).games 1
$scoreboard players add @s mgs.st.mp.$(gamemode).wins 1

