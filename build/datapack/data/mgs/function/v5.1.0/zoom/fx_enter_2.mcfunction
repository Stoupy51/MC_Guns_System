
#> mgs:v5.1.0/zoom/fx_enter_2
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zoom/fx_enter
#

posteffect add @s mgs:zoom_2
scoreboard players set @s mgs.zoom_fx 2
scoreboard players reset @s mgs.zoom_fx_off

