
#> mgs:v5.0.0/multiplayer/editor/set_secondary_full
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/pick_secondary_scope with storage mgs:temp editor
#
# @args		secondary (unknown)
#			secondary_scope (unknown)
#

$data modify storage mgs:temp editor.secondary_full set value "$(secondary)$(secondary_scope)"

