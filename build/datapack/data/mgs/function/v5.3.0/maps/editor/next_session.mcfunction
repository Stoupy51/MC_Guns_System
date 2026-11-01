
#> mgs:v5.3.0/maps/editor/next_session
#
# @within	mgs:v5.3.0/maps/editor/enter
#			mgs:v5.3.0/maps/editor/cleanup
#

execute unless entity @a[scores={mgs.mp.map_edit=1}] run scoreboard players add #ed_session mgs.data 1

