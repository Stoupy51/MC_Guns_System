
#> mgs:v5.1.0/zombies/inventory/on_new_item
#
# @within	#common_signals:signals/on_new_item
#

# Kill any non-zombies-slot managed drop from zombies players (@s = the item entity).
# Both item checks MUST run before `on origin`: past it @s is the thrower, so a check on @s Item
# always passed and `kill @s` killed the PLAYER instead of the drop (grenade drop = instant death).
execute unless data entity @s Item.components."minecraft:custom_data".mgs run return 0
execute if data entity @s Item.components."minecraft:custom_data".mgs.zombies run return 0

# Thrown by an in-game zombies player? -> the drop is unmanaged, remove it
scoreboard players set #zb_drop_kill mgs.data 0
execute on origin if score @s mgs.zb.in_game matches 1 run scoreboard players set #zb_drop_kill mgs.data 1
execute if score #zb_drop_kill mgs.data matches 1 run kill @s

