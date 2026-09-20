
#> mgs:v5.1.0/zoom/crosshair_add
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zoom/crosshair_first with storage mgs:input crosshair
#
# @args		from (int)
#			to (int)
#

$posteffect add @s mgs:crosshair_$(from)_$(to)

