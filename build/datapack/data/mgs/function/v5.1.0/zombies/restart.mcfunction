
#> mgs:v5.1.0/zombies/restart
#
# @within	string in mgs:v5.1.0/zombies/game_over
#

# Roster = players still in the game; if the auto-stop already cleared in_game, fall back to the
# snapshot game_over took. Tag them so the roster survives the stop cleanup below.
execute if entity @a[scores={mgs.zb.in_game=1}] run tag @a[scores={mgs.zb.in_game=1}] add mgs.zb_restart
execute unless entity @a[scores={mgs.zb.in_game=1}] run tag @a[tag=mgs.zb_last_roster] add mgs.zb_restart
execute unless entity @a[tag=mgs.zb_restart] run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.nothing_to_restart_no_players_from_the_last_game","color":"red"}]

# Bail before tearing anything down if no map is selected (start would reject it anyway).
execute if data storage mgs:zombies game{map_id:""} run return run function mgs:v5.1.0/zombies/restart_no_map

# Cancel the pending auto-stop from game_over, then run the normal teardown.
schedule clear mgs:v5.1.0/zombies/stop
function mgs:v5.1.0/zombies/stop

# Re-opt the roster back in (stop set in_game 0) and start fresh — stop kept game.map_id / variant.
scoreboard players set @a[tag=mgs.zb_restart] mgs.zb.in_game 1
tag @a[tag=mgs.zb_restart] remove mgs.zb_restart
tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.an_operator_restarted_the_game","color":"yellow"}]
function mgs:v5.1.0/zombies/start

