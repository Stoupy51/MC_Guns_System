
#> mgs:v5.0.0/zombies/feedback/sound_box_spin
#
# @executed	as @n[tag=mgs.mystery_box_active] & at @s
#
# @within	mgs:v5.0.0/zombies/mystery_box/try_use [ as @n[tag=mgs.mystery_box_active] & at @s ]
#

playsound mgs:zombies/mystery_box/box_spin ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.1 1.0
playsound mgs:zombies/mystery_box/music_box ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0

