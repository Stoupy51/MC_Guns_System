
#> mgs:v5.3.0/zoom/fx_enter
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/zoom/set
#

# @s = a player who just entered aim-down-sights
scoreboard players set #zoom_sight mgs.data 0
function mgs:v5.3.0/zoom/fx_sight with storage mgs:gun all.stats.models
function mgs:v5.3.0/zoom/fx_clear
execute if score #zoom_sight mgs.data matches 0 run function mgs:v5.3.0/zoom/fx_enter_zoom_iron
execute if score #zoom_sight mgs.data matches 1 run function mgs:v5.3.0/zoom/fx_enter_zoom_kobra
execute if score #zoom_sight mgs.data matches 2 run function mgs:v5.3.0/zoom/fx_enter_zoom_holo
execute if score #zoom_sight mgs.data matches 3 run function mgs:v5.3.0/zoom/fx_enter_zoom_acog
execute if score #zoom_sight mgs.data matches 4 run function mgs:v5.3.0/zoom/fx_enter_zoom_aug
execute if score #zoom_sight mgs.data matches 5 run function mgs:v5.3.0/zoom/fx_enter_zoom_mk4
execute if score #zoom_sight mgs.data matches 6 run function mgs:v5.3.0/zoom/fx_enter_zoom_pu
execute if score #zoom_sight mgs.data matches 7 run function mgs:v5.3.0/zoom/fx_enter_zoom_pso

