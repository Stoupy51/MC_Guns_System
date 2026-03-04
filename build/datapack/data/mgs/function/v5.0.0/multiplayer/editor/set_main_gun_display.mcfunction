
#> mgs:v5.0.0/multiplayer/editor/set_main_gun_display
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/save with storage mgs:temp editor
#
# @args		primary_name (unknown)
#			primary_scope_name (unknown)
#

$data modify storage mgs:temp _new_loadout.main_gun_display set value "$(primary_name) ($(primary_scope_name))"

