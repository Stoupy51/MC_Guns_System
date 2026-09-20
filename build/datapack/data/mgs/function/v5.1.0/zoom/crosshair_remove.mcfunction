
#> mgs:v5.1.0/zoom/crosshair_remove
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zoom/crosshair_clear with storage mgs:input crosshair
#
# @args		from (int)
#			to (int)
#

$posteffect remove @s mgs:crosshair_$(from)_$(to)

