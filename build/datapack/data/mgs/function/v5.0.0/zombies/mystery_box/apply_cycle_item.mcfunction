
#> mgs:v5.0.0/zombies/mystery_box/apply_cycle_item
#
# @executed	as @e[tag=mgs.mb_display,limit=1]
#
# @within	mgs:v5.0.0/zombies/mystery_box/cycle_display [ as @e[tag=mgs.mb_display,limit=1] ]
#

# Set item display to the cycled weapon's display item
data modify entity @s item set from storage mgs:temp _mb_cycle_iter[0].display_item

