
#> mgs:v5.1.0/shared/drops/place_mag
#
# @executed	at @e[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/shared/drops/give_mag with storage mgs:temp _give
#
# @args		slot (unknown)
#

$item replace entity @s inventory.$(slot) from entity @n[tag=mgs.drop_mag_helper] contents

