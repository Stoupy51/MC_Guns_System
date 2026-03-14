
#> mgs:v5.0.0/multiplayer/editor/notify_saved
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/save with storage mgs:temp editor
#
# @args		primary_name (unknown)
#			secondary_name (unknown)
#

$tellraw @s ["",[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],[{"text":"","color":"white"},{"translate":"mgs.loadout_saved"},": "],{"text":"$(primary_name) + $(secondary_name)","color":"green","bold":true}]

