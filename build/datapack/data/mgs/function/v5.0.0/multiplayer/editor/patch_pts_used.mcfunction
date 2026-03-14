
#> mgs:v5.0.0/multiplayer/editor/patch_pts_used
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/show_confirm with storage mgs:temp
#
# @args		_pts_used (unknown)
#

$data modify storage mgs:temp dialog.body[0].contents set value ["","",{"translate":"mgs.points_used"},": ",{"text":"$(_pts_used)","color":"gold","bold":true},{"text":" / 10","color":"dark_gray"}]

