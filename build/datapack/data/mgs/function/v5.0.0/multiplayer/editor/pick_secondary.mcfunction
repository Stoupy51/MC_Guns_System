
#> mgs:v5.0.0/multiplayer/editor/pick_secondary
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Store secondary weapon choice
execute if score @s mgs.player.config matches 250 run data modify storage mgs:temp editor merge value {secondary:"m1911",secondary_name:"M1911",secondary_mag:"m1911_mag",secondary_mag_count:2,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_full:"m1911"}
execute if score @s mgs.player.config matches 251 run data modify storage mgs:temp editor merge value {secondary:"m9",secondary_name:"M9",secondary_mag:"m9_mag",secondary_mag_count:2,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_full:"m9"}
execute if score @s mgs.player.config matches 252 run data modify storage mgs:temp editor merge value {secondary:"deagle",secondary_name:"Deagle",secondary_mag:"deagle_mag",secondary_mag_count:2,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_full:"deagle"}
execute if score @s mgs.player.config matches 253 run data modify storage mgs:temp editor merge value {secondary:"makarov",secondary_name:"Makarov",secondary_mag:"makarov_mag",secondary_mag_count:2,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_full:"makarov"}
execute if score @s mgs.player.config matches 254 run data modify storage mgs:temp editor merge value {secondary:"glock17",secondary_name:"Glock 17",secondary_mag:"glock17_mag",secondary_mag_count:2,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_full:"glock17"}
execute if score @s mgs.player.config matches 255 run data modify storage mgs:temp editor merge value {secondary:"glock18",secondary_name:"Glock 18",secondary_mag:"glock18_mag",secondary_mag_count:2,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_full:"glock18"}
execute if score @s mgs.player.config matches 256 run data modify storage mgs:temp editor merge value {secondary:"vz61",secondary_name:"VZ-61",secondary_mag:"vz61_mag",secondary_mag_count:2,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_full:"vz61"}
execute if score @s mgs.player.config matches 258 run data modify storage mgs:temp editor merge value {secondary:"",secondary_name:"None",secondary_scope:"",secondary_scope_name:"",secondary_full:"",secondary_mag:"",secondary_mag_count:0}

# Check budget before deducting (secondary weapon costs 1 pt; None is free)
execute unless data storage mgs:temp editor{secondary:""} if score @s mgs.mp.edit_points matches ..0 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.not_enough_points_for_a_secondary_weapon","color":"red"}]

# Deduct cost if a secondary was chosen
execute unless data storage mgs:temp editor{secondary:""} run scoreboard players remove @s mgs.mp.edit_points 1

# Route: none → skip to equip slot 1, deagle → scope, others → secondary mag count
execute if data storage mgs:temp editor{secondary:""} run return run function mgs:v5.0.0/multiplayer/editor/show_equip_slot1_dialog
execute if data storage mgs:temp editor{secondary:"deagle"} run return run function mgs:v5.0.0/multiplayer/editor/scope/secondary_4only

# No scope variants: go directly to secondary mag count
function mgs:v5.0.0/multiplayer/editor/show_secondary_mags_dialog

