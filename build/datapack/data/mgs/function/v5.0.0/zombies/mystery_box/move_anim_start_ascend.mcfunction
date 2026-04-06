
#> mgs:v5.0.0/zombies/mystery_box/move_anim_start_ascend
#
# @within	mgs:v5.0.0/zombies/mystery_box/move_anim_tick
#

# Enable smooth movement on chest and bear displays
data merge entity @n[tag=mgs.mb_presence] {teleport_duration:5}
data merge entity @n[tag=mgs.mb_display] {teleport_duration:5}
execute as @n[tag=mgs.mystery_box_active] at @s run function mgs:v5.0.0/zombies/feedback/sound_box_disappear

