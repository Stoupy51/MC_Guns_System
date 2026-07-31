
#> mgs:v5.1.0/multiplayer/gamemodes/demo/next_round
#
# @executed	as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/attackers_win
#			mgs:v5.1.0/multiplayer/gamemodes/demo/defenders_win
#

# The clock is reset here as well as in start_round: the tick stops driving #mp_timer between rounds, so
# the 3s gap would otherwise sit on the expired value.
scoreboard players set #mp_timer mgs.data 3600
tag @a remove mgs.demo_atk

scoreboard players add #demo_round mgs.data 1

# End of the first half: swap sides and play the second
execute if score #demo_round mgs.data matches 2 run function mgs:v5.1.0/multiplayer/gamemodes/demo/swap_sides
execute if score #demo_round mgs.data matches 2 run return run schedule function mgs:v5.1.0/multiplayer/gamemodes/demo/start_round 60t

# Both halves played: a leader takes the match, a tie goes to sudden death
execute if score #demo_round mgs.data matches 3 if score #red mgs.mp.team > #blue mgs.mp.team run return run function mgs:v5.1.0/multiplayer/team_wins {team:"Red"}
execute if score #demo_round mgs.data matches 3 if score #blue mgs.mp.team > #red mgs.mp.team run return run function mgs:v5.1.0/multiplayer/team_wins {team:"Blue"}
execute if score #demo_round mgs.data matches 3 run return run function mgs:v5.1.0/multiplayer/gamemodes/demo/start_overtime

# Overtime itself expired without a detonation
function mgs:v5.1.0/multiplayer/game_draw

