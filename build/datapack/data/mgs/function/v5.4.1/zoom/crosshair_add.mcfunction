
#> mgs:v5.4.1/zoom/crosshair_add
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zoom/crosshair_first with storage mgs:input crosshair
#			mgs:v5.4.1/zoom/crosshair_to_back with storage mgs:input crosshair
#
# @args		from (int)
#			to (int)
#

$posteffect add @s mgs:crosshair_$(from)_$(to)

