
#> mgs:v5.0.0/zombies/feedback/sound_box_disappear
#
# @executed	as @n[tag=mgs.mystery_box_active] & at @s
#
# @within	mgs:v5.0.0/zombies/mystery_box/move_anim_start_ascend [ as @n[tag=mgs.mystery_box_active] & at @s ]
#

playsound mgs:zombies/mystery_box/disappear ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0

