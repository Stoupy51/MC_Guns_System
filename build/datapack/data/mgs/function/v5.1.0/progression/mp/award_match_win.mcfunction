
#> mgs:v5.1.0/progression/mp/award_match_win
#
# @executed	as @a[scores={mgs.mp.in_game=1},tag=mgs.xp_winner]
#
# @within	mgs:v5.1.0/multiplayer/xp/on_game_end [ as @a[scores={mgs.mp.in_game=1},tag=mgs.xp_winner] ]
#

# Match win, to every player on the winning side
scoreboard players add @s mgs.mp.xp_total 50
scoreboard players add @s mgs.mp.xp_prog 50
scoreboard players add @s mgs.mp.xp_session 50
function mgs:v5.1.0/progression/mp/settle

