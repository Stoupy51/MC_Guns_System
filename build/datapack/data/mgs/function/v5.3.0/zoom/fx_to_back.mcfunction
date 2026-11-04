
#> mgs:v5.3.0/zoom/fx_to_back
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/player/apply_flash
#			mgs:v5.3.0/player/apply_pap_flash
#

# Post effects run in list order. The flash lights the scene from the unmagnified depth buffer,
# so it has to run before the zoom, or its lighting lands on the wrong blocks once magnified.
execute if score @s mgs.zoom_fx matches 1 run posteffect remove @s mgs:zoom_iron
execute if score @s mgs.zoom_fx matches 1 run posteffect add @s mgs:zoom_iron
execute if score @s mgs.zoom_fx matches -1 run posteffect remove @s mgs:zoom_iron_out
execute if score @s mgs.zoom_fx matches -1 run posteffect add @s mgs:zoom_iron_out
execute if score @s mgs.zoom_fx matches 2 run posteffect remove @s mgs:zoom_kobra
execute if score @s mgs.zoom_fx matches 2 run posteffect add @s mgs:zoom_kobra
execute if score @s mgs.zoom_fx matches -2 run posteffect remove @s mgs:zoom_kobra_out
execute if score @s mgs.zoom_fx matches -2 run posteffect add @s mgs:zoom_kobra_out
execute if score @s mgs.zoom_fx matches 3 run posteffect remove @s mgs:zoom_holo
execute if score @s mgs.zoom_fx matches 3 run posteffect add @s mgs:zoom_holo
execute if score @s mgs.zoom_fx matches -3 run posteffect remove @s mgs:zoom_holo_out
execute if score @s mgs.zoom_fx matches -3 run posteffect add @s mgs:zoom_holo_out
execute if score @s mgs.zoom_fx matches 4 run posteffect remove @s mgs:zoom_acog
execute if score @s mgs.zoom_fx matches 4 run posteffect add @s mgs:zoom_acog
execute if score @s mgs.zoom_fx matches -4 run posteffect remove @s mgs:zoom_acog_out
execute if score @s mgs.zoom_fx matches -4 run posteffect add @s mgs:zoom_acog_out
execute if score @s mgs.zoom_fx matches 5 run posteffect remove @s mgs:zoom_aug
execute if score @s mgs.zoom_fx matches 5 run posteffect add @s mgs:zoom_aug
execute if score @s mgs.zoom_fx matches -5 run posteffect remove @s mgs:zoom_aug_out
execute if score @s mgs.zoom_fx matches -5 run posteffect add @s mgs:zoom_aug_out
execute if score @s mgs.zoom_fx matches 6 run posteffect remove @s mgs:zoom_mk4
execute if score @s mgs.zoom_fx matches 6 run posteffect add @s mgs:zoom_mk4
execute if score @s mgs.zoom_fx matches -6 run posteffect remove @s mgs:zoom_mk4_out
execute if score @s mgs.zoom_fx matches -6 run posteffect add @s mgs:zoom_mk4_out
execute if score @s mgs.zoom_fx matches 7 run posteffect remove @s mgs:zoom_pu
execute if score @s mgs.zoom_fx matches 7 run posteffect add @s mgs:zoom_pu
execute if score @s mgs.zoom_fx matches -7 run posteffect remove @s mgs:zoom_pu_out
execute if score @s mgs.zoom_fx matches -7 run posteffect add @s mgs:zoom_pu_out
execute if score @s mgs.zoom_fx matches 8 run posteffect remove @s mgs:zoom_pso
execute if score @s mgs.zoom_fx matches 8 run posteffect add @s mgs:zoom_pso
execute if score @s mgs.zoom_fx matches -8 run posteffect remove @s mgs:zoom_pso_out
execute if score @s mgs.zoom_fx matches -8 run posteffect add @s mgs:zoom_pso_out

