
#> mgs:v5.4.2/zoom/crosshair_replace
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zoom/crosshair_swap with storage mgs:input crosshair
#
# @args		from (int)
#			to (int)
#			next (int)
#

$posteffect remove @s mgs:crosshair_$(from)_$(to)
$posteffect add @s mgs:crosshair_$(to)_$(next)

