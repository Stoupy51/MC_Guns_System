
#> mgs:v5.4.0/zombies/inventory/swap_slots
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/inventory/move_found_slot {from:"$(from)",to:"$(to)"}
#
# @args		to (string)
#			from (string)
#

# Run as the temporary item_display; the player is @p[tag=mgs.inv_swapping].
$item replace entity @s contents from entity @p[tag=mgs.inv_swapping] $(to)
$item replace entity @p[tag=mgs.inv_swapping] $(to) from entity @p[tag=mgs.inv_swapping] $(from)
$execute if items entity @s contents * run item replace entity @p[tag=mgs.inv_swapping] $(from) from entity @s contents
$execute unless items entity @s contents * run item replace entity @p[tag=mgs.inv_swapping] $(from) with air
kill @s

