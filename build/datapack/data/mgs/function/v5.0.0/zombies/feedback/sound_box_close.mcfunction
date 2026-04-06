
#> mgs:v5.0.0/zombies/feedback/sound_box_close
#
# @executed	as @n[tag=mgs.mystery_box_active] & at @s
#
# @within	mgs:v5.0.0/zombies/mystery_box/collect [ as @n[tag=mgs.mystery_box_active] & at @s ]
#

playsound mgs:zombies/mystery_box/close ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.9 1.0

