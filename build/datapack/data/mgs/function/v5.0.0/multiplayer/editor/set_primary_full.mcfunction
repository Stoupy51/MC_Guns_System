
#> mgs:v5.0.0/multiplayer/editor/set_primary_full
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/pick_primary_scope with storage mgs:temp editor
#
# @args		primary (unknown)
#			primary_scope (unknown)
#

$data modify storage mgs:temp editor.primary_full set value "$(primary)$(primary_scope)"

