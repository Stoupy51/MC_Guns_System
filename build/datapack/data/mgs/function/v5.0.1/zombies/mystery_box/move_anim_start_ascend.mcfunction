
#> mgs:v5.0.1/zombies/mystery_box/move_anim_start_ascend
#
# @within	mgs:v5.0.1/zombies/mystery_box/move_anim_tick
#

# Enable smooth movement on chest (base + lid) and bear displays
execute as @e[tag=mgs.mb_presence] run data merge entity @s {teleport_duration:5}
data merge entity @n[tag=mgs.mb_display] {teleport_duration:5}
execute as @n[tag=mgs.mystery_box_active] at @s run function mgs:v5.0.1/zombies/feedback/sound_box_disappear

