
#> mgs:v5.0.0/zombies/inventory/on_new_item
#
# @within	#common_signals:signals/on_new_item
#

# Kill any non-zombies-slot managed drop from zombies players.
execute if data entity @s Item.components."minecraft:custom_data".mgs on origin if score @s mgs.zb.in_game matches 1 unless data entity @s Item.components."minecraft:custom_data".mgs.zombies run kill @s

