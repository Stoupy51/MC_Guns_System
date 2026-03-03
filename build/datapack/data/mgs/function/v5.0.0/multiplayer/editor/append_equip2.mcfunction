
#> mgs:v5.0.0/multiplayer/editor/append_equip2
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/save with storage mgs:temp editor
#
# @args		equip_slot2 (string)
#

$data modify storage mgs:temp _new_loadout.slots append value {slot:"hotbar.7",loot:"mgs:i/$(equip_slot2)",count:1,consumable:0b,bullets:0}

