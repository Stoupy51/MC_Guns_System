
#> mgs:v5.4.2/players/mi_remove
#
# @within	mgs:v5.4.2/dialog/close_then
#			string in mgs:v5.4.2/players/row_missions
#

scoreboard players set @s mgs.mi.in_game 0
scoreboard players set @s mgs.mp.team 0
team leave @s
execute if data storage mgs:missions game{state:"active"} run gamemode spectator @s
tellraw @s [{"translate":"mgs.removed_from_the_mission","fallback":"Removed from the mission","color":"gray"}]

