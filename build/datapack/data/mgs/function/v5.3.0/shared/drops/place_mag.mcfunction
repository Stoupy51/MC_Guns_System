
#> mgs:v5.3.0/shared/drops/place_mag
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/shared/drops/give_mag with storage mgs:temp _give
#
# @args		slot (unknown)
#

$item replace entity @s inventory.$(slot) from entity @n[tag=mgs.drop_mag_helper] contents

