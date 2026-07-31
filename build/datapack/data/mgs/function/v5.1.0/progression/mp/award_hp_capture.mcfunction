
#> mgs:v5.1.0/progression/mp/award_hp_capture
#
# @executed	as @a[tag=mgs.in_hp_zone,scores={mgs.mp.team=1,mgs.mp.in_game=1}]
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/hp/score_tick [ as @a[tag=mgs.in_hp_zone,scores={mgs.mp.team=1,mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/gamemodes/hp/score_tick [ as @a[tag=mgs.in_hp_zone,scores={mgs.mp.team=2,mgs.mp.in_game=1}] ]
#

# First hold of a Hardpoint hill after it rotates
scoreboard players add @s mgs.mp.xp_total 20
scoreboard players add @s mgs.mp.xp_prog 20
scoreboard players add @s mgs.mp.xp_session 20
function mgs:v5.1.0/progression/mp/settle

