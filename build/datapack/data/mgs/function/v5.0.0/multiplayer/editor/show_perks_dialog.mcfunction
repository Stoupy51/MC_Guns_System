
#> mgs:v5.0.0/multiplayer/editor/show_perks_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#			mgs:v5.0.0/multiplayer/editor/pick_equip_slot2
#			mgs:v5.0.0/multiplayer/editor/pick_perk
#

scoreboard players set @s mgs.mp.edit_step 9
execute store result storage mgs:temp _pts int 1 run scoreboard players get @s mgs.mp.edit_points

# Determine which perks are selected
execute if data storage mgs:temp editor{perks:["quick_reload"]} run data modify storage mgs:temp _perk_0 set value 1
execute unless data storage mgs:temp editor{perks:["quick_reload"]} run data modify storage mgs:temp _perk_0 set value 0
execute if data storage mgs:temp editor{perks:["quick_swap"]} run data modify storage mgs:temp _perk_1 set value 1
execute unless data storage mgs:temp editor{perks:["quick_swap"]} run data modify storage mgs:temp _perk_1 set value 0
execute if data storage mgs:temp editor{perks:["infinite_ammo"]} run data modify storage mgs:temp _perk_2 set value 1
execute unless data storage mgs:temp editor{perks:["infinite_ammo"]} run data modify storage mgs:temp _perk_2 set value 0

# Count selected perks
scoreboard players set #perk_count mgs.data 0
execute if data storage mgs:temp editor{perks:["quick_reload"]} run scoreboard players add #perk_count mgs.data 1
execute if data storage mgs:temp editor{perks:["quick_swap"]} run scoreboard players add #perk_count mgs.data 1
execute if data storage mgs:temp editor{perks:["infinite_ammo"]} run scoreboard players add #perk_count mgs.data 1

execute store result storage mgs:temp _perk_count int 1 run scoreboard players get #perk_count mgs.data

function mgs:v5.0.0/multiplayer/editor/show_perks_dialog_macro with storage mgs:temp

