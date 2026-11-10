
#> mgs:v5.4.1/player/hit_dir_add
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/player/hit_dir_show with storage mgs:input hit_dir
#			mgs:v5.4.1/player/hit_dir_to_back with storage mgs:input hit_dir
#
# @args		sector (int)
#			slot (int)
#

$posteffect add @s mgs:hit_dir_$(sector)_$(slot)

