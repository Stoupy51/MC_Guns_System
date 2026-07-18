
#> mgs:v5.1.0/players/zb_remove
#
# @within	mgs:v5.1.0/players/row_zombies
#

scoreboard players set @s mgs.zb.in_game 0
team leave @s
execute if data storage mgs:zombies game{state:"active"} run gamemode spectator @s
tellraw @s [{"translate":"mgs.removed_from_the_zombies_game","color":"gray"}]

