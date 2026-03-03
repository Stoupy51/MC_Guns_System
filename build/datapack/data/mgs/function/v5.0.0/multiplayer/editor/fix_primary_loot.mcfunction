
#> mgs:v5.0.0/multiplayer/editor/fix_primary_loot
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/save with storage mgs:temp editor
#
# @args		primary_full (unknown)
#

$data modify storage mgs:temp _build.primary_data.gun_slot.loot set value "mgs:i/$(primary_full)"

