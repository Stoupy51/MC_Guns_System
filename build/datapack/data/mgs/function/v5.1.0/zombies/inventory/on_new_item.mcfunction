
#> mgs:v5.1.0/zombies/inventory/on_new_item
#
# @within	#common_signals:signals/on_new_item
#

# Run as the item entity: kill unmanaged drops thrown by zombies players. The item checks must run before `on origin`,
# where @s becomes the thrower and `kill @s` would kill the player.
execute unless data entity @s Item.components."minecraft:custom_data".mgs run return 0
execute if data entity @s Item.components."minecraft:custom_data".mgs.zombies run return 0

scoreboard players set #zb_drop_kill mgs.data 0
execute on origin if score @s mgs.zb.in_game matches 1 run scoreboard players set #zb_drop_kill mgs.data 1
execute if score #zb_drop_kill mgs.data matches 1 run kill @s

