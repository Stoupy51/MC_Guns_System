
#> mgs:v5.1.0/multiplayer/gamemodes/demo/next_round
#
# @executed	as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/attackers_win
#			mgs:v5.1.0/multiplayer/gamemodes/demo/defenders_win
#

# Also reset here: the tick does not drive #mp_timer between rounds.
scoreboard players set #mp_timer mgs.data 3600
tag @a remove mgs.demo_atk

scoreboard players add #demo_round mgs.data 1

# End of the first half: swap sides.
execute if score #demo_round mgs.data matches 2 run function mgs:v5.1.0/multiplayer/gamemodes/demo/swap_sides
execute if score #demo_round mgs.data matches 2 run return run schedule function mgs:v5.1.0/multiplayer/gamemodes/demo/start_round 60t

# Each round awards one point, so this ends the match on 2-0, or on 2-1 after the decider; only 1-1 falls through.
execute if score #red mgs.mp.team > #blue mgs.mp.team run return run function mgs:v5.1.0/multiplayer/team_wins {team:"Red"}
execute if score #blue mgs.mp.team > #red mgs.mp.team run return run function mgs:v5.1.0/multiplayer/team_wins {team:"Blue"}

# Still level: the decider, its defending side chosen by kills.
execute if score #demo_round mgs.data matches 3 run function mgs:v5.1.0/multiplayer/gamemodes/demo/pick_tiebreak_sides
execute if score #demo_round mgs.data matches 3 run return run schedule function mgs:v5.1.0/multiplayer/gamemodes/demo/start_round 60t

# Unreachable: every round awards a point.
function mgs:v5.1.0/multiplayer/game_draw

