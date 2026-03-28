
#> mgs:v5.0.0/multiplayer/gamemodes/hp/cleanup
#
# @within	mgs:v5.0.0/multiplayer/stop
#

kill @e[tag=mgs.hp_marker]
kill @e[tag=mgs.hp_label]
tag @a remove mgs.in_hp_zone

