
#> mgs:v5.0.1/zombies/mystery_box/move_anim_start_ascend
#
# @within	mgs:v5.0.1/zombies/mystery_box/move_anim_tick
#

# Enable smooth movement on the active chest (base + lid) and the bear display only
execute as @e[tag=mgs.mb_presence,tag=!mgs.mb_temp] run data merge entity @s {teleport_duration:5}
execute as @e[tag=mgs.mb_bear] run data merge entity @s {teleport_duration:5}
execute as @n[tag=mgs.mystery_box_active] at @s run function mgs:v5.0.1/zombies/feedback/sound_box_disappear

