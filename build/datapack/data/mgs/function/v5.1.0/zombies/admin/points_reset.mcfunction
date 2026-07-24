
#> mgs:v5.1.0/zombies/admin/points_reset
#
# @executed	as the player & at current position
#
# @within	dialog mgs:v5.1.0/zombies/admin
#

execute unless data storage mgs:zombies game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_zombies_game_is_active","color":"red"}]
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.zb.points 0
tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.an_operator_reset_everyones_points","color":"red"}]

