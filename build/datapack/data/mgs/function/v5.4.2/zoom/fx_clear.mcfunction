
#> mgs:v5.4.2/zoom/fx_clear
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zoom/fx_enter
#

execute if score @s mgs.zoom_fx matches 1 run posteffect remove @s mgs:zoom_iron
execute if score @s mgs.zoom_fx matches -1 run posteffect remove @s mgs:zoom_iron_out
execute if score @s mgs.zoom_fx matches 2 run posteffect remove @s mgs:zoom_acog
execute if score @s mgs.zoom_fx matches -2 run posteffect remove @s mgs:zoom_acog_out
execute if score @s mgs.zoom_fx matches 3 run posteffect remove @s mgs:zoom_mk4
execute if score @s mgs.zoom_fx matches -3 run posteffect remove @s mgs:zoom_mk4_out
execute if score @s mgs.zoom_fx matches 4 run posteffect remove @s mgs:zoom_pu
execute if score @s mgs.zoom_fx matches -4 run posteffect remove @s mgs:zoom_pu_out
execute if score @s mgs.zoom_fx matches 5 run posteffect remove @s mgs:zoom_pso
execute if score @s mgs.zoom_fx matches -5 run posteffect remove @s mgs:zoom_pso_out
scoreboard players set @s mgs.zoom_fx 0
scoreboard players reset @s mgs.zoom_fx_off

