
#> mgs:v5.4.1/multiplayer/editor/notify_saved
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/editor/save with storage mgs:temp editor
#
# @args		primary_name (unknown)
#			secondary_name (unknown)
#

$tellraw @s ["",[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],[{"text":"","color":"white"},{"translate":"mgs.loadout_saved","fallback":"Loadout saved"},": "],{"text":"$(primary_name) + $(secondary_name)","color":"green","bold":true}]

