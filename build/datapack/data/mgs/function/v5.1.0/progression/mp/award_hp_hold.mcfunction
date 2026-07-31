
#> mgs:v5.1.0/progression/mp/award_hp_hold
#
# @executed	as @a[tag=mgs.in_hp_zone,scores={mgs.mp.team=1,mgs.mp.in_game=1}]
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/hp/score_tick [ as @a[tag=mgs.in_hp_zone,scores={mgs.mp.team=1,mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/gamemodes/hp/score_tick [ as @a[tag=mgs.in_hp_zone,scores={mgs.mp.team=2,mgs.mp.in_game=1}] ]
#

# Standing in the active hill, once per 5s
scoreboard players add @s mgs.mp.xp_total 1
scoreboard players add @s mgs.mp.xp_prog 1
scoreboard players add @s mgs.mp.xp_session 1
function mgs:v5.1.0/progression/mp/settle

