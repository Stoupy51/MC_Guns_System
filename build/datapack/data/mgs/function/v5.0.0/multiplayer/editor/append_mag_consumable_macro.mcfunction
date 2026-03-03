
#> mgs:v5.0.0/multiplayer/editor/append_mag_consumable_macro
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/append_mag_consumable with storage mgs:temp
#
# @args		_inv_n (unknown)
#			_mag_id (unknown)
#			_mag_bullets (unknown)
#

$data modify storage mgs:temp _new_loadout.slots append value {slot:"inventory.$(_inv_n)",loot:"mgs:i/$(_mag_id)",count:1,consumable:1b,bullets:$(_mag_bullets)}

