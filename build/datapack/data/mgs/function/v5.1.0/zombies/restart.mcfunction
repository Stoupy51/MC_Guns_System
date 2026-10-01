
#> mgs:v5.1.0/zombies/restart
#
# @executed	as the player & at current position
#
# @within	string in mgs:v5.1.0/zombies/game_over
#			dialog mgs:v5.1.0/zombies/setup
#

# Roster: players still in game, else the snapshot game_over took. Tagged so it survives the stop below.
execute if entity @a[scores={mgs.zb.in_game=1}] run tag @a[scores={mgs.zb.in_game=1}] add mgs.zb_restart
execute unless entity @a[scores={mgs.zb.in_game=1}] run tag @a[tag=mgs.zb_last_roster] add mgs.zb_restart
execute unless entity @a[tag=mgs.zb_restart] run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.nothing_to_restart_no_players_from_the_last_game","color":"red"}]

# Before tearing anything down.
execute if data storage mgs:zombies game{map_id:""} run return run function mgs:v5.1.0/zombies/restart_no_map

# Cancels the auto-stop scheduled by game_over.
schedule clear mgs:v5.1.0/zombies/stop
function mgs:v5.1.0/zombies/stop

# stop kept game.map_id and the variant.
scoreboard players set @a[tag=mgs.zb_restart] mgs.zb.in_game 1
tag @a[tag=mgs.zb_restart] remove mgs.zb_restart
tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.an_operator_restarted_the_game","color":"yellow"}]
function mgs:v5.1.0/zombies/start

