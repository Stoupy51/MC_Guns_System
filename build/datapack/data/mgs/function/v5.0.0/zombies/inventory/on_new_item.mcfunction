
#> mgs:v5.0.0/zombies/inventory/on_new_item
#
# @within	#common_signals:signals/on_new_item
#

# Kill any mgs item dropped by a player in a zombies game
execute if data entity @s Item.components."minecraft:custom_data".mgs on origin if score @s mgs.zb.in_game matches 1 run kill @s

