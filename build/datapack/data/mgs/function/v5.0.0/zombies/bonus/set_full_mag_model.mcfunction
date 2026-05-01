
#> mgs:v5.0.0/zombies/bonus/set_full_mag_model
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.0.0/zombies/bonus/refill_magazine with storage mgs:temp refill
#			mgs:v5.0.0/zombies/pap/upgrade_magazine_slot with storage mgs:temp refill
#
# @args		slot (unknown)
#			mag_model (unknown)
#

$item modify entity @s $(slot) {"function":"minecraft:set_components", "components":{"minecraft:item_model":"$(mag_model)"}}

