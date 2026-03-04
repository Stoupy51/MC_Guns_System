
#> mgs:v5.0.0/multiplayer/editor/set_sec_gun_display
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/save with storage mgs:temp editor
#
# @args		secondary_name (unknown)
#			secondary_scope_name (unknown)
#

$data modify storage mgs:temp _new_loadout.secondary_gun_display set value "$(secondary_name) ($(secondary_scope_name))"

