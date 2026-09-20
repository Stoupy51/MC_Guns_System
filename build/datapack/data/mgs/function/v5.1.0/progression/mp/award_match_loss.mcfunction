
#> mgs:v5.1.0/progression/mp/award_match_loss
#
# @executed	as @a[scores={mgs.mp.in_game=1},tag=!mgs.xp_winner]
#
# @within	mgs:v5.1.0/multiplayer/xp/on_game_end [ as @a[scores={mgs.mp.in_game=1},tag=!mgs.xp_winner] ]
#

# Match loss or draw, to everyone who played it
scoreboard players add @s mgs.mp.xp_total 20
scoreboard players add @s mgs.mp.xp_prog 20
scoreboard players add @s mgs.mp.xp_session 20
function mgs:v5.1.0/progression/mp/settle

