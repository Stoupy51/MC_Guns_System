
#> mgs:v5.4.4/multiplayer/gamemodes/hp/cleanup
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/multiplayer/stop
#

kill @e[tag=mgs.hp_marker]
kill @e[tag=mgs.hp_label]
tag @a remove mgs.in_hp_zone

