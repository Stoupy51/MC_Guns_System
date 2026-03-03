
#> mgs:v5.0.0/multiplayer/editor/back_to_secondary
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Refund secondary mags cost (secondary_mag_count * COST_SECONDARY_MAG)
execute store result score #refund_mags mgs.data run data get storage mgs:temp editor.secondary_mag_count
scoreboard players operation @s mgs.mp.edit_points += #refund_mags mgs.data
# Refund scope cost if a scope was selected
execute if data storage mgs:temp editor{secondary_scope:"_1"} run scoreboard players add @s mgs.mp.edit_points 1
execute if data storage mgs:temp editor{secondary_scope:"_2"} run scoreboard players add @s mgs.mp.edit_points 1
execute if data storage mgs:temp editor{secondary_scope:"_3"} run scoreboard players add @s mgs.mp.edit_points 1
execute if data storage mgs:temp editor{secondary_scope:"_4"} run scoreboard players add @s mgs.mp.edit_points 1
# Refund secondary weapon cost if one was selected
execute unless data storage mgs:temp editor{secondary:""} run scoreboard players add @s mgs.mp.edit_points 1
# Clear secondary state
data modify storage mgs:temp editor.secondary set value ""
data modify storage mgs:temp editor.secondary_scope set value ""
data modify storage mgs:temp editor.secondary_mag_count set value 0
# Show secondary dialog
function mgs:v5.0.0/multiplayer/editor/show_secondary_dialog

