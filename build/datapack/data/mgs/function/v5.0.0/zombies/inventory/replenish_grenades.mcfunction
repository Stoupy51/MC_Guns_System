
#> mgs:v5.0.0/zombies/inventory/replenish_grenades
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.0.0/zombies/start_round [ as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] ]
#

# Only if player has a grenade in hotbar.7
execute unless items entity @s hotbar.7 *[custom_data~{mgs:{gun:true}}] run return fail

# Read current remaining bullets from grenade (hotbar.7 = Slot 7b in player NBT)
execute store result score #nade_rem mgs.data run data get entity @s Inventory[{Slot:7b}].components."minecraft:custom_data".mgs.stats.remaining_bullets

# Add 2, cap at 4
scoreboard players add #nade_rem mgs.data 2
execute if score #nade_rem mgs.data matches 5.. run scoreboard players set #nade_rem mgs.data 4

# Apply via item modifier
execute store result storage mgs:temp zb_item_stats.remaining_bullets int 1 run scoreboard players get #nade_rem mgs.data
data modify storage mgs:temp zb_item_stats.capacity set value 4
item modify entity @s hotbar.7 mgs:v5.0.0/zb_item_stats

