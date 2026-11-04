
#> mgs:v5.3.0/zoom/fx_clear
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zoom/fx_enter
#

execute if score @s mgs.zoom_fx matches 2 run posteffect remove @s mgs:zoom_2
execute if score @s mgs.zoom_fx matches -2 run posteffect remove @s mgs:zoom_2_out
execute if score @s mgs.zoom_fx matches 3 run posteffect remove @s mgs:zoom_3
execute if score @s mgs.zoom_fx matches -3 run posteffect remove @s mgs:zoom_3_out
execute if score @s mgs.zoom_fx matches 4 run posteffect remove @s mgs:zoom_4
execute if score @s mgs.zoom_fx matches -4 run posteffect remove @s mgs:zoom_4_out
scoreboard players set @s mgs.zoom_fx 0
scoreboard players reset @s mgs.zoom_fx_off

