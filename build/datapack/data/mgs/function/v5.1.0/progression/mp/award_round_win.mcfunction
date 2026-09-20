
#> mgs:v5.1.0/progression/mp/award_round_win
#
# @executed	as @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}]
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/attackers_win [ as @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/gamemodes/snd/attackers_win [ as @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/gamemodes/snd/defenders_win [ as @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/gamemodes/snd/defenders_win [ as @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/gamemodes/demo/attackers_win [ as @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/gamemodes/demo/attackers_win [ as @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/gamemodes/demo/defenders_win [ as @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/gamemodes/demo/defenders_win [ as @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] ]
#

# Winning an S&D or Demolition round
scoreboard players add @s mgs.mp.xp_total 20
scoreboard players add @s mgs.mp.xp_prog 20
scoreboard players add @s mgs.mp.xp_session 20
function mgs:v5.1.0/progression/mp/settle

