
#> mgs:v5.0.0/zombies/mystery_box/spawn_display_finalize
#
# @within	mgs:v5.0.0/zombies/mystery_box/spawn_display 5t append [ scheduled ]
#

data merge entity @n[tag=mgs.mb_display_new] {transformation:{translation:[0f,0.8f,0f]},start_interpolation:0,interpolation_duration:200}
tag @n[tag=mgs.mb_display_new] remove mgs.mb_display_new

