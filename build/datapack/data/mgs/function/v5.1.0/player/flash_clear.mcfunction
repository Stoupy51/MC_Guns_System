
#> mgs:v5.1.0/player/flash_clear
#
# @executed	at @s & anchored eyes & positioned ^ ^ ^0.001 & as @a[distance=..16]
#
# @within	mgs:v5.1.0/player/apply_flash_if_can_see
#			mgs:v5.1.0/player/apply_pap_flash_if_can_see
#			mgs:v5.1.0/player/flash_tick
#

execute if score @s mgs.flash_id matches 1 run posteffect remove @s mgs:flash_0
execute if score @s mgs.flash_id matches 2 run posteffect remove @s mgs:flash_1
execute if score @s mgs.flash_id matches 3 run posteffect remove @s mgs:flash_zoom_0
execute if score @s mgs.flash_id matches 4 run posteffect remove @s mgs:flash_zoom_1
execute if score @s mgs.flash_id matches 5 run posteffect remove @s mgs:flash_pap_0
execute if score @s mgs.flash_id matches 6 run posteffect remove @s mgs:flash_pap_1
execute if score @s mgs.flash_id matches 7 run posteffect remove @s mgs:flash_pap_zoom_0
execute if score @s mgs.flash_id matches 8 run posteffect remove @s mgs:flash_pap_zoom_1
scoreboard players set @s mgs.flash_id 0

