
#> mgs:v5.1.0/multiplayer/pickup_place_mag
#
# @executed	at @e[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/multiplayer/pickup_give_mag with storage mgs:temp _give
#
# @args		slot (unknown)
#

$item replace entity @s inventory.$(slot) from entity @n[tag=mgs.mp_mag_helper] contents

