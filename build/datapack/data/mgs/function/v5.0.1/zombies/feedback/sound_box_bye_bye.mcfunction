
#> mgs:v5.0.1/zombies/feedback/sound_box_bye_bye
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.0.1/zombies/mystery_box/show_bear_result
#

execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/mystery_box/bye_bye ambient @s ~ ~ ~ 1.0 1.0

