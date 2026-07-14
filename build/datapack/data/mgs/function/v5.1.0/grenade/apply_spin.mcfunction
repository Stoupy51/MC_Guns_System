
#> mgs:v5.1.0/grenade/apply_spin
#
# @executed	as @e[tag=mgs.grenade] & at @s
#
# @within	mgs:v5.1.0/grenade/spin_tick with storage mgs:temp _gr_spin
#
# @args		angle (unknown)
#

$data modify entity @s transformation.left_rotation set value {axis:[1f,0f,0f],angle:$(angle)}
data merge entity @s {start_interpolation:0,interpolation_duration:1}

