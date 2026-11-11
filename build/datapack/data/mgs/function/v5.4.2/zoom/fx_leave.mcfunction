
#> mgs:v5.4.2/zoom/fx_leave
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zoom/remove
#			mgs:v5.4.2/zoom/clear_state
#			mgs:v5.4.2/zoom/check_slowness
#

# Hand the ramp over to the matching fade-out id, which plays itself out and is retired by fx_tick
execute unless score @s mgs.zoom_fx matches 1.. run return 0
execute if score @s mgs.zoom_fx matches 1 run posteffect remove @s mgs:zoom_iron
execute if score @s mgs.zoom_fx matches 1 run posteffect add @s mgs:zoom_iron_out
execute if score @s mgs.zoom_fx matches 1 run scoreboard players set @s mgs.zoom_fx -1
execute if score @s mgs.zoom_fx matches 2 run posteffect remove @s mgs:zoom_acog
execute if score @s mgs.zoom_fx matches 2 run posteffect add @s mgs:zoom_acog_out
execute if score @s mgs.zoom_fx matches 2 run scoreboard players set @s mgs.zoom_fx -2
execute if score @s mgs.zoom_fx matches 3 run posteffect remove @s mgs:zoom_mk4
execute if score @s mgs.zoom_fx matches 3 run posteffect add @s mgs:zoom_mk4_out
execute if score @s mgs.zoom_fx matches 3 run scoreboard players set @s mgs.zoom_fx -3
execute if score @s mgs.zoom_fx matches 4 run posteffect remove @s mgs:zoom_pu
execute if score @s mgs.zoom_fx matches 4 run posteffect add @s mgs:zoom_pu_out
execute if score @s mgs.zoom_fx matches 4 run scoreboard players set @s mgs.zoom_fx -4
execute if score @s mgs.zoom_fx matches 5 run posteffect remove @s mgs:zoom_pso
execute if score @s mgs.zoom_fx matches 5 run posteffect add @s mgs:zoom_pso_out
execute if score @s mgs.zoom_fx matches 5 run scoreboard players set @s mgs.zoom_fx -5
scoreboard players set @s mgs.zoom_fx_off 5
function mgs:v5.4.2/player/hit_dir_to_back

