
#> mgs:v5.0.0/zombies/inventory/do_swap_1
#
# @executed	as the player & at current position
#
# @within	mgs:v5.0.0/zombies/inventory/swap_to_1 {from:"$(from)"}
#
# @args		from (string)
#

# Copy the weapon from source slot to item_display
$item replace entity @s contents from entity @p[tag=mgs.inv_fix] $(from)
# Move whatever is in hotbar.1 to source slot
$item replace entity @p[tag=mgs.inv_fix] $(from) from entity @p[tag=mgs.inv_fix] hotbar.1
# Move weapon from item_display to hotbar.1
item replace entity @p[tag=mgs.inv_fix] hotbar.1 from entity @s contents
kill @s

