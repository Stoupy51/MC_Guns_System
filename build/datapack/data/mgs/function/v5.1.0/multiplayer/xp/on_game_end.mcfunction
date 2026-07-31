
#> mgs:v5.1.0/multiplayer/xp/on_game_end
#
# @within	#mgs:multiplayer/on_game_end
#

execute if score #red mgs.mp.team > #blue mgs.mp.team run tag @a[scores={mgs.mp.team=1}] add mgs.xp_winner
execute if score #blue mgs.mp.team > #red mgs.mp.team run tag @a[scores={mgs.mp.team=2}] add mgs.xp_winner

execute as @a[scores={mgs.mp.in_game=1},tag=mgs.xp_winner] run function mgs:v5.1.0/progression/mp/award_match_win
execute as @a[scores={mgs.mp.in_game=1},tag=!mgs.xp_winner] run function mgs:v5.1.0/progression/mp/award_match_loss
tag @a remove mgs.xp_winner

