
#> mgs:v5.1.0/multiplayer/drop_held_weapon
#
# @executed	at @s
#
# @within	mgs:v5.1.0/multiplayer/enter_death_spectate [ at @s ]
#			mgs:v5.1.0/missions/enter_death_spectate [ at @s ]
#

# Only drop a gun held in a weapon slot (hotbar.1 or hotbar.2; hotbar.0 is the knife)
execute store result score #drop_sel mgs.data run data get entity @s SelectedItemSlot
execute unless score #drop_sel mgs.data matches 1..2 run scoreboard players set #drop_sel mgs.data 1
execute if score #drop_sel mgs.data matches 1 unless items entity @s hotbar.1 *[custom_data~{mgs:{gun:true}}] run return 0
execute if score #drop_sel mgs.data matches 2 unless items entity @s hotbar.2 *[custom_data~{mgs:{gun:true}}] run return 0

# Capture the held gun item (strip the inventory Slot tag so it fits an item_display / item entity)
data remove storage mgs:temp _dropw
execute if score #drop_sel mgs.data matches 1 run data modify storage mgs:temp _dropw set from entity @s Inventory[{Slot:1b}]
execute if score #drop_sel mgs.data matches 2 run data modify storage mgs:temp _dropw set from entity @s Inventory[{Slot:2b}]
data remove storage mgs:temp _dropw.Slot

# The live bullet count lives on the scoreboard, not in the item (<= 0 makes the drop use half a mag)
scoreboard players operation #drop_ammo mgs.data = @s mgs.remaining_bullets
function mgs:v5.1.0/shared/drops/drop

