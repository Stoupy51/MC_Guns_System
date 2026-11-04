
#> mgs:v5.3.0/zombies/admin/points_add_500000
#
# @within	mgs:v5.3.0/dialog/close_then
#			dialog mgs:v5.3.0/zombies/admin
#

execute unless data storage mgs:zombies game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.no_zombies_game_is_active","fallback":"No zombies game is active.","color":"red"}]
scoreboard players add @a[scores={mgs.zb.in_game=1}] mgs.zb.points 500000
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.an_operator_granted_500000_points_to_everyone","fallback":"An operator granted 500000 points to everyone.","color":"green"}]

