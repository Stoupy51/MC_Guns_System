
#> mgs:v5.0.0/zombies/feedback/sound_box_bye_bye
#
# @executed	as @n[tag=mgs.mystery_box_active] & at @s
#
# @within	mgs:v5.0.0/zombies/mystery_box/show_bear_result [ as @n[tag=mgs.mystery_box_active] & at @s ]
#

execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/mystery_box/bye_bye ambient @s ~ ~ ~ 1.0 1.0

