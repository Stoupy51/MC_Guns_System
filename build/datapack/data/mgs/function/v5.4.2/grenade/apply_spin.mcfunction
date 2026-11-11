
#> mgs:v5.4.2/grenade/apply_spin
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/grenade/spin_tick with storage mgs:temp _gr_spin
#
# @args		angle (unknown)
#

$data modify entity @s transformation.left_rotation set value {axis:[1f,0f,0f],angle:$(angle)}
data merge entity @s {start_interpolation:0,interpolation_duration:1}

