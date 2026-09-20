
#> mgs:v5.1.0/zoom/crosshair_replace
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zoom/crosshair_swap with storage mgs:input crosshair
#
# @args		from (int)
#			to (int)
#			next (int)
#

$posteffect remove @s mgs:crosshair_$(from)_$(to)
$posteffect add @s mgs:crosshair_$(to)_$(next)

