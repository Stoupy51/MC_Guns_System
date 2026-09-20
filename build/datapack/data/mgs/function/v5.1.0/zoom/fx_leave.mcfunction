
#> mgs:v5.1.0/zoom/fx_leave
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zoom/remove
#			mgs:v5.1.0/zoom/clear_state
#			mgs:v5.1.0/zoom/check_slowness
#

# Hand the ramp over to the matching fade-out id, which plays itself out and is retired by fx_tick
execute unless score @s mgs.zoom_fx matches 1.. run return 0
execute if score @s mgs.zoom_fx matches 2 run posteffect remove @s mgs:zoom_2
execute if score @s mgs.zoom_fx matches 2 run posteffect add @s mgs:zoom_2_out
execute if score @s mgs.zoom_fx matches 2 run scoreboard players set @s mgs.zoom_fx -2
execute if score @s mgs.zoom_fx matches 3 run posteffect remove @s mgs:zoom_3
execute if score @s mgs.zoom_fx matches 3 run posteffect add @s mgs:zoom_3_out
execute if score @s mgs.zoom_fx matches 3 run scoreboard players set @s mgs.zoom_fx -3
execute if score @s mgs.zoom_fx matches 4 run posteffect remove @s mgs:zoom_4
execute if score @s mgs.zoom_fx matches 4 run posteffect add @s mgs:zoom_4_out
execute if score @s mgs.zoom_fx matches 4 run scoreboard players set @s mgs.zoom_fx -4
scoreboard players set @s mgs.zoom_fx_off 5

