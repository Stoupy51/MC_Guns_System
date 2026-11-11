
#> mgs:v5.4.2/player/stamina_burn
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/player/stamina_bar
#

scoreboard players remove @s mgs.stam_sat 8
execute if score @s mgs.stam_sat matches ..-1 run scoreboard players set @s mgs.stam_sat 0
effect give @s minecraft:hunger 1 255 true

