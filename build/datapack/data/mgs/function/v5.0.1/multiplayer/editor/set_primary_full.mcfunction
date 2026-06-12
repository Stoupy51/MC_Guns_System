
#> mgs:v5.0.1/multiplayer/editor/set_primary_full
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/multiplayer/editor/pick_primary_camo with storage mgs:temp editor
#
# @args		primary (unknown)
#			primary_scope (unknown)
#			primary_camo (unknown)
#

$data modify storage mgs:temp editor.primary_full set value "$(primary)$(primary_scope)$(primary_camo)"

