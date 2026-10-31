
#> mgs:v5.3.0/progression/mp/award_match_win
#
# @executed	as @a[scores={mgs.mp.in_game=1},tag=mgs.xp_winner]
#
# @within	mgs:v5.3.0/multiplayer/xp/on_game_end [ as @a[scores={mgs.mp.in_game=1},tag=mgs.xp_winner] ]
#

# Match win, to every player on the winning side
scoreboard players add @s mgs.mp.xp_total 50
scoreboard players add @s mgs.mp.xp_prog 50
scoreboard players add @s mgs.mp.xp_session 50

# Observers of this award
scoreboard players add @s mgs.adv.mp.wins 1
function mgs:v5.3.0/progression/adv/mp/wins/check
function mgs:v5.3.0/progression/mp/settle

scoreboard players add @s mgs.st.mp.games 1
function mgs:v5.3.0/stats/mp/gamemode_win with storage mgs:multiplayer game

