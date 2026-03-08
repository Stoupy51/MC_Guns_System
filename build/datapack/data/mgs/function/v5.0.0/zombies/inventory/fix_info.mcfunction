
#> mgs:v5.0.0/zombies/inventory/fix_info
#
# @executed	as the player & at current position
#
# @within	mgs:v5.0.0/zombies/inventory/check_slots
#

clear @s *[custom_data~{mgs:{zb_info:true}}]
function mgs:v5.0.0/zombies/inventory/refresh_info_item

