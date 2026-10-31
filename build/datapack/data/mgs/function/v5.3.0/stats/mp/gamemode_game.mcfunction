
#> mgs:v5.3.0/stats/mp/gamemode_game
#
# @executed	as @a[scores={mgs.mp.in_game=1},tag=!mgs.xp_winner]
#
# @within	mgs:v5.3.0/progression/mp/award_match_loss with storage mgs:multiplayer game
#
# @args		gamemode (unknown)
#

$scoreboard players add @s mgs.st.mp.$(gamemode).games 1

