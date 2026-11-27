
#> mgs:v5.4.4/player/config/hitmarker_sound
#
# @within	#mgs:signals/damage
#			mgs:v5.4.4/dialog/close_then
#

execute as @a[tag=mgs.ticking] unless score @s mgs.player.hitmarker matches 0 at @s run playsound mgs:common/hitmarker player @s ~ ~ ~ 0.6
# Skipped when already played through ticking.
execute as @a[tag=mgs.temp_shooter,tag=!mgs.ticking] unless score @s mgs.player.hitmarker matches 0 at @s run playsound mgs:common/hitmarker player @s ~ ~ ~ 0.6

