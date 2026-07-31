
#> mgs:v5.1.0/multiplayer/gamemodes/demo/overtime_won
#
# @executed	as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/site_destroyed
#

execute unless score #demo_round_active mgs.data matches 1 run return fail
scoreboard players set #demo_round_active mgs.data 0

execute if score #demo_last_owner mgs.data matches 1 run scoreboard players add #red mgs.mp.team 1
execute if score #demo_last_owner mgs.data matches 2 run scoreboard players add #blue mgs.mp.team 1
execute if score #demo_last_owner mgs.data matches 1 run return run function mgs:v5.1.0/multiplayer/team_wins {team:"Red"}
execute if score #demo_last_owner mgs.data matches 2 run return run function mgs:v5.1.0/multiplayer/team_wins {team:"Blue"}

# Nobody owned it (should be unreachable): treat it as the draw an expired overtime would have been
function mgs:v5.1.0/multiplayer/game_draw

