
#> mgs:v5.1.0/players/mp_remove
#
# @within	string in mgs:v5.1.0/players/row_multiplayer
#

scoreboard players set @s mgs.mp.team 0
scoreboard players set @s mgs.mp.in_game 0
team leave @s
execute if data storage mgs:multiplayer game{state:"active"} run gamemode spectator @s
tellraw @s [{"translate":"mgs.removed_from_the_game","color":"gray"}]

