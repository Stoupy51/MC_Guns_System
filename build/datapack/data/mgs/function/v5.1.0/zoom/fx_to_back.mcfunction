
#> mgs:v5.1.0/zoom/fx_to_back
#
# @executed	at @s & anchored eyes & positioned ^ ^ ^0.001 & as @a[distance=..16]
#
# @within	mgs:v5.1.0/player/apply_flash_if_can_see
#			mgs:v5.1.0/player/apply_pap_flash_if_can_see
#

# Post effects run in list order. The flash lights the scene from the unmagnified depth buffer,
# so it has to run before the zoom, or its lighting lands on the wrong blocks once magnified.
execute if score @s mgs.zoom_fx matches 2 run posteffect remove @s mgs:zoom_2
execute if score @s mgs.zoom_fx matches 2 run posteffect add @s mgs:zoom_2
execute if score @s mgs.zoom_fx matches -2 run posteffect remove @s mgs:zoom_2_out
execute if score @s mgs.zoom_fx matches -2 run posteffect add @s mgs:zoom_2_out
execute if score @s mgs.zoom_fx matches 3 run posteffect remove @s mgs:zoom_3
execute if score @s mgs.zoom_fx matches 3 run posteffect add @s mgs:zoom_3
execute if score @s mgs.zoom_fx matches -3 run posteffect remove @s mgs:zoom_3_out
execute if score @s mgs.zoom_fx matches -3 run posteffect add @s mgs:zoom_3_out
execute if score @s mgs.zoom_fx matches 4 run posteffect remove @s mgs:zoom_4
execute if score @s mgs.zoom_fx matches 4 run posteffect add @s mgs:zoom_4
execute if score @s mgs.zoom_fx matches -4 run posteffect remove @s mgs:zoom_4_out
execute if score @s mgs.zoom_fx matches -4 run posteffect add @s mgs:zoom_4_out

