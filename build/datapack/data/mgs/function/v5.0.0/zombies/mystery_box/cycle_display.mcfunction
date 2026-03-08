
#> mgs:v5.0.0/zombies/mystery_box/cycle_display
#
# @within	mgs:v5.0.0/zombies/mystery_box/tick
#

# Pick a random item from pool to display
execute store result score #mb_cycle mgs.data run random value 0..100
execute store result score #mb_ps mgs.data run data get storage mgs:zombies mystery_box_pool
scoreboard players operation #mb_cycle mgs.data %= #mb_ps mgs.data

data modify storage mgs:temp _mb_cycle_iter set from storage mgs:zombies mystery_box_pool
function mgs:v5.0.0/zombies/mystery_box/cycle_iterate

# Apply the cycled item directly to the display entity
data modify entity @n[tag=mgs.mb_display] item set from storage mgs:temp _mb_cycle_iter[0].display_item

