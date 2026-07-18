
#> mgs:v5.1.0/players/mi_remove
#
# @within	mgs:v5.1.0/players/row_missions
#

scoreboard players set @s mgs.mi.in_game 0
scoreboard players set @s mgs.mp.team 0
team leave @s
execute if data storage mgs:missions game{state:"active"} run gamemode spectator @s
tellraw @s [{"translate":"mgs.removed_from_the_mission","color":"gray"}]

