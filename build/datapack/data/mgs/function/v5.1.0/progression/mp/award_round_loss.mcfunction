
#> mgs:v5.1.0/progression/mp/award_round_loss
#
# @executed	as @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}]
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/snd/attackers_win [ as @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/gamemodes/snd/attackers_win [ as @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/gamemodes/snd/defenders_win [ as @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/gamemodes/snd/defenders_win [ as @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/gamemodes/demo/attackers_win [ as @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/gamemodes/demo/attackers_win [ as @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/gamemodes/demo/defenders_win [ as @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] ]
#			mgs:v5.1.0/multiplayer/gamemodes/demo/defenders_win [ as @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] ]
#

# Losing one; never zero, so a losing side still progresses
scoreboard players add @s mgs.mp.xp_total 5
scoreboard players add @s mgs.mp.xp_prog 5
scoreboard players add @s mgs.mp.xp_session 5
function mgs:v5.1.0/progression/mp/settle

