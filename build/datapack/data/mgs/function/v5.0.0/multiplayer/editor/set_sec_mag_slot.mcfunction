
#> mgs:v5.0.0/multiplayer/editor/set_sec_mag_slot
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/append_sec_mags with storage mgs:temp
#
# @args		_inv_n (unknown)
#

$data modify storage mgs:temp _sec_mag.slot set value "inventory.$(_inv_n)"

