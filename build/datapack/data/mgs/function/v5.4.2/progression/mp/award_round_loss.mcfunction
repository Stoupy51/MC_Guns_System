
#> mgs:v5.4.2/progression/mp/award_round_loss
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/gamemodes/snd/attackers_win [ as @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] ]
#			mgs:v5.4.2/multiplayer/gamemodes/snd/attackers_win [ as @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] ]
#			mgs:v5.4.2/multiplayer/gamemodes/snd/defenders_win [ as @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] ]
#			mgs:v5.4.2/multiplayer/gamemodes/snd/defenders_win [ as @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] ]
#			mgs:v5.4.2/multiplayer/gamemodes/demo/attackers_win [ as @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] ]
#			mgs:v5.4.2/multiplayer/gamemodes/demo/attackers_win [ as @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] ]
#			mgs:v5.4.2/multiplayer/gamemodes/demo/defenders_win [ as @a[scores={mgs.mp.team=1,mgs.mp.in_game=1}] ]
#			mgs:v5.4.2/multiplayer/gamemodes/demo/defenders_win [ as @a[scores={mgs.mp.team=2,mgs.mp.in_game=1}] ]
#

# Losing one; never zero, so a losing side still progresses
scoreboard players add @s mgs.mp.xp_total 5
scoreboard players add @s mgs.mp.xp_prog 5
scoreboard players add @s mgs.mp.xp_session 5
function mgs:v5.4.2/progression/mp/settle

