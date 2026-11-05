
#> mgs:v5.3.0/zoom/fx_tick
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/player/tick
#			mgs:v5.3.0/dialog/close_then
#

# @s = a player whose fade-out is still applied
scoreboard players remove @s mgs.zoom_fx_off 1
execute if score @s mgs.zoom_fx_off matches 1.. run return 0
execute if score @s mgs.zoom_fx matches -1 run posteffect remove @s mgs:zoom_iron_out
execute if score @s mgs.zoom_fx matches -2 run posteffect remove @s mgs:zoom_acog_out
execute if score @s mgs.zoom_fx matches -3 run posteffect remove @s mgs:zoom_mk4_out
execute if score @s mgs.zoom_fx matches -4 run posteffect remove @s mgs:zoom_pu_out
execute if score @s mgs.zoom_fx matches -5 run posteffect remove @s mgs:zoom_pso_out
scoreboard players set @s mgs.zoom_fx 0
scoreboard players reset @s mgs.zoom_fx_off

