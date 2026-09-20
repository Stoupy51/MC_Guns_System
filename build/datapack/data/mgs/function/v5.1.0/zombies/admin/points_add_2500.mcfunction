
#> mgs:v5.1.0/zombies/admin/points_add_2500
#
# @executed	as the player & at current position
#
# @within	dialog mgs:v5.1.0/zombies/admin
#

execute unless data storage mgs:zombies game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_zombies_game_is_active","color":"red"}]
scoreboard players add @a[scores={mgs.zb.in_game=1}] mgs.zb.points 2500
tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.an_operator_granted_2500_points_to_everyone","color":"green"}]

