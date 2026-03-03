
#> mgs:v5.0.0/multiplayer/editor/toggle_perk_0
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/pick_perk
#

# Check if already selected → remove (refund) and early-exit
execute if data storage mgs:temp editor{perks:["quick_reload"]} run scoreboard players add @s mgs.mp.edit_points 1
execute if data storage mgs:temp editor{perks:["quick_reload"]} run return run function mgs:v5.0.0/multiplayer/editor/remove_perk_0

# Check max perks limit
scoreboard players set #perk_count mgs.data 0
execute if data storage mgs:temp editor{perks:["quick_reload"]} run scoreboard players add #perk_count mgs.data 1
execute if data storage mgs:temp editor{perks:["quick_swap"]} run scoreboard players add #perk_count mgs.data 1
execute if data storage mgs:temp editor{perks:["infinite_ammo"]} run scoreboard players add #perk_count mgs.data 1

execute if score #perk_count mgs.data matches 3.. run return run tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.max_3_perks_allowed","color":"red"}]

# Check points budget
execute if score @s mgs.mp.edit_points matches ..0 run return run tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.not_enough_points","color":"red"}]

# Add perk and deduct points
data modify storage mgs:temp editor.perks append value "quick_reload"
scoreboard players remove @s mgs.mp.edit_points 1

