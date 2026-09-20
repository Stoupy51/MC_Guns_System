
#> mgs:v5.1.0/zoom/fx_enter_4
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zoom/fx_enter
#

posteffect add @s mgs:zoom_4
scoreboard players set @s mgs.zoom_fx 4
scoreboard players reset @s mgs.zoom_fx_off

