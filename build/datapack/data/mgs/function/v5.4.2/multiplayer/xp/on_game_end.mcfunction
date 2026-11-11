
#> mgs:v5.4.2/multiplayer/xp/on_game_end
#
# @within	#mgs:multiplayer/on_game_end
#			mgs:v5.4.2/dialog/close_then
#

execute if score #red mgs.mp.team > #blue mgs.mp.team run tag @a[scores={mgs.mp.in_game=1,mgs.mp.team=1}] add mgs.xp_winner
execute if score #blue mgs.mp.team > #red mgs.mp.team run tag @a[scores={mgs.mp.in_game=1,mgs.mp.team=2}] add mgs.xp_winner

execute as @a[scores={mgs.mp.in_game=1},tag=mgs.xp_winner] run function mgs:v5.4.2/progression/mp/award_match_win
execute as @a[scores={mgs.mp.in_game=1},tag=!mgs.xp_winner] run function mgs:v5.4.2/progression/mp/award_match_loss

# Needs the winner tag, so it runs before the cleanup.
execute as @a[scores={mgs.mp.in_game=1,mgs.mp.deaths=0},tag=mgs.xp_winner] run advancement grant @s only mgs:challenges/mp/flawless
tag @a remove mgs.xp_winner

