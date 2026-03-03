
#> mgs:v5.0.0/multiplayer/editor/append_mag_regular
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/append_mag_loop with storage mgs:temp
#
# @args		_inv_n (unknown)
#			_mag_id (unknown)
#

$data modify storage mgs:temp _new_loadout.slots append value {slot:"inventory.$(_inv_n)",loot:"mgs:i/$(_mag_id)",count:1,consumable:0b,bullets:0}

