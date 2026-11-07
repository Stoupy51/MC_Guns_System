
#> mgs:v5.4.0/player/stamina_swim_drain
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/player/stamina_tick
#

scoreboard players add @s mgs.stam_swim 1
execute if score @s mgs.stam_swim matches 5.. run scoreboard players set @s mgs.stam_swim 0
execute if score @s mgs.stam_swim matches 0 run scoreboard players remove @s mgs.stam 2

