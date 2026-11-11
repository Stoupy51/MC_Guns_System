
#> mgs:v5.4.2/zombies/admin/points_add_2500
#
# @within	mgs:v5.4.2/dialog/close_then
#			dialog mgs:v5.4.2/zombies/admin
#

execute unless data storage mgs:zombies game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.no_zombies_game_is_active","fallback":"No zombies game is active.","color":"red"}]
scoreboard players add @a[scores={mgs.zb.in_game=1}] mgs.zb.points 2500
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.an_operator_granted_2500_points_to_everyone","fallback":"An operator granted 2500 points to everyone.","color":"green"}]

