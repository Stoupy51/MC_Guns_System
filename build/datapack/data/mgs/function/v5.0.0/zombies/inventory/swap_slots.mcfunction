
#> mgs:v5.0.0/zombies/inventory/swap_slots
#
# @executed	as the player & at current position
#
# @within	mgs:v5.0.0/zombies/inventory/move_found_slot {from:"$(from)",to:"$(to)"}
#
# @args		to (string)
#			from (string)
#

# @s = temp item_display, player = @p[tag=mgs.inv_swapping]
# Save target item to temp display
$item replace entity @s contents from entity @p[tag=mgs.inv_swapping] $(to)
# Move source to target
$item replace entity @p[tag=mgs.inv_swapping] $(to) from entity @p[tag=mgs.inv_swapping] $(from)
# Put old target item (from display) into source, or clear source if target was empty
$execute if items entity @s contents * run item replace entity @p[tag=mgs.inv_swapping] $(from) from entity @s contents
$execute unless items entity @s contents * run item replace entity @p[tag=mgs.inv_swapping] $(from) with air
kill @s

