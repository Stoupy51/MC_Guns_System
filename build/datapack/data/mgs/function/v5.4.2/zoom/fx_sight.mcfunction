
#> mgs:v5.4.2/zoom/fx_sight
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zoom/fx_enter with storage mgs:gun all.stats.models
#
# @args		zoom (unknown)
#

$execute store result score #zoom_sight mgs.data run data get storage mgs:data zoom_sights."$(zoom)"

