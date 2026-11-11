
#> mgs:v5.4.2/maps/editor/next_session
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/enter
#			mgs:v5.4.2/maps/editor/cleanup
#

execute unless entity @a[scores={mgs.mp.map_edit=1}] run scoreboard players add #ed_session mgs.data 1

