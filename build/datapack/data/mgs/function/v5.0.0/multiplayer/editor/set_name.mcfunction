
#> mgs:v5.0.0/multiplayer/editor/set_name
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/save with storage mgs:temp editor
#
# @args		primary_name (unknown)
#			secondary_name (unknown)
#

$data modify storage mgs:temp _new_loadout.name set value "$(primary_name) + $(secondary_name)"

