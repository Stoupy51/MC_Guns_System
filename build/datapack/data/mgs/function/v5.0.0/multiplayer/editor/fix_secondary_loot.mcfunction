
#> mgs:v5.0.0/multiplayer/editor/fix_secondary_loot
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/save with storage mgs:temp editor
#
# @args		secondary_full (unknown)
#

$data modify storage mgs:temp _build.secondary_data.fixed_slots[0].loot set value "mgs:i/$(secondary_full)"

