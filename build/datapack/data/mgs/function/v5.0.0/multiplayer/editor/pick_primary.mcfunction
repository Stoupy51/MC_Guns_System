
#> mgs:v5.0.0/multiplayer/editor/pick_primary
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Store primary weapon choice based on trigger value
execute if score @s mgs.player.config matches 200 run data modify storage mgs:temp editor set value {primary:"ak47",primary_name:"AK-47",primary_mag:"ak47_mag",primary_mag_count:3,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"ak47"}
execute if score @s mgs.player.config matches 201 run data modify storage mgs:temp editor set value {primary:"m16a4",primary_name:"M16A4",primary_mag:"m16a4_mag",primary_mag_count:3,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"m16a4"}
execute if score @s mgs.player.config matches 202 run data modify storage mgs:temp editor set value {primary:"famas",primary_name:"FAMAS",primary_mag:"famas_mag",primary_mag_count:3,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"famas"}
execute if score @s mgs.player.config matches 203 run data modify storage mgs:temp editor set value {primary:"aug",primary_name:"AUG",primary_mag:"aug_mag",primary_mag_count:3,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"aug"}
execute if score @s mgs.player.config matches 204 run data modify storage mgs:temp editor set value {primary:"m4a1",primary_name:"M4A1",primary_mag:"m4a1_mag",primary_mag_count:3,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"m4a1"}
execute if score @s mgs.player.config matches 205 run data modify storage mgs:temp editor set value {primary:"fnfal",primary_name:"FN FAL",primary_mag:"fnfal_mag",primary_mag_count:3,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"fnfal"}
execute if score @s mgs.player.config matches 206 run data modify storage mgs:temp editor set value {primary:"g3a3",primary_name:"G3A3",primary_mag:"g3a3_mag",primary_mag_count:3,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"g3a3"}
execute if score @s mgs.player.config matches 207 run data modify storage mgs:temp editor set value {primary:"scar17",primary_name:"SCAR-17",primary_mag:"scar17_mag",primary_mag_count:3,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"scar17"}
execute if score @s mgs.player.config matches 208 run data modify storage mgs:temp editor set value {primary:"mp5",primary_name:"MP5",primary_mag:"mp5_mag",primary_mag_count:4,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"mp5"}
execute if score @s mgs.player.config matches 209 run data modify storage mgs:temp editor set value {primary:"mp7",primary_name:"MP7",primary_mag:"mp7_mag",primary_mag_count:4,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"mp7"}
execute if score @s mgs.player.config matches 210 run data modify storage mgs:temp editor set value {primary:"mac10",primary_name:"MAC-10",primary_mag:"mac10_mag",primary_mag_count:4,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"mac10"}
execute if score @s mgs.player.config matches 211 run data modify storage mgs:temp editor set value {primary:"ppsh41",primary_name:"PPSh-41",primary_mag:"ppsh41_mag",primary_mag_count:3,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"ppsh41"}
execute if score @s mgs.player.config matches 212 run data modify storage mgs:temp editor set value {primary:"sten",primary_name:"Sten",primary_mag:"sten_mag",primary_mag_count:3,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"sten"}
execute if score @s mgs.player.config matches 213 run data modify storage mgs:temp editor set value {primary:"m249",primary_name:"M249",primary_mag:"m249_mag",primary_mag_count:3,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"m249"}
execute if score @s mgs.player.config matches 214 run data modify storage mgs:temp editor set value {primary:"rpk",primary_name:"RPK",primary_mag:"rpk_mag",primary_mag_count:3,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"rpk"}
execute if score @s mgs.player.config matches 215 run data modify storage mgs:temp editor set value {primary:"svd",primary_name:"SVD",primary_mag:"svd_mag",primary_mag_count:3,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"svd"}
execute if score @s mgs.player.config matches 216 run data modify storage mgs:temp editor set value {primary:"m82",primary_name:"M82",primary_mag:"m82_mag",primary_mag_count:3,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"m82"}
execute if score @s mgs.player.config matches 217 run data modify storage mgs:temp editor set value {primary:"mosin",primary_name:"Mosin-Nagant",primary_mag:"mosin_bullet",primary_mag_count:10,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"mosin"}
execute if score @s mgs.player.config matches 218 run data modify storage mgs:temp editor set value {primary:"m24",primary_name:"M24",primary_mag:"m24_bullet",primary_mag_count:10,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"m24"}
execute if score @s mgs.player.config matches 219 run data modify storage mgs:temp editor set value {primary:"spas12",primary_name:"SPAS-12",primary_mag:"spas12_shell",primary_mag_count:16,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"spas12"}
execute if score @s mgs.player.config matches 220 run data modify storage mgs:temp editor set value {primary:"m500",primary_name:"M500",primary_mag:"m500_shell",primary_mag_count:12,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"m500"}
execute if score @s mgs.player.config matches 221 run data modify storage mgs:temp editor set value {primary:"m590",primary_name:"M590",primary_mag:"m590_shell",primary_mag_count:16,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"m590"}
execute if score @s mgs.player.config matches 222 run data modify storage mgs:temp editor set value {primary:"rpg7",primary_name:"RPG-7",primary_mag:"rpg7_rocket",primary_mag_count:3,primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"rpg7"}

# Route: weapons with scope variants go to scope dialog, others skip to secondary
execute if data storage mgs:temp editor{primary:"ak47"} run return run function mgs:v5.0.0/multiplayer/editor/scope/primary_full
execute if data storage mgs:temp editor{primary:"m16a4"} run return run function mgs:v5.0.0/multiplayer/editor/scope/primary_full
execute if data storage mgs:temp editor{primary:"famas"} run return run function mgs:v5.0.0/multiplayer/editor/scope/primary_full
execute if data storage mgs:temp editor{primary:"aug"} run return run function mgs:v5.0.0/multiplayer/editor/scope/primary_full
execute if data storage mgs:temp editor{primary:"m4a1"} run return run function mgs:v5.0.0/multiplayer/editor/scope/primary_full
execute if data storage mgs:temp editor{primary:"fnfal"} run return run function mgs:v5.0.0/multiplayer/editor/scope/primary_full
execute if data storage mgs:temp editor{primary:"g3a3"} run return run function mgs:v5.0.0/multiplayer/editor/scope/primary_full
execute if data storage mgs:temp editor{primary:"scar17"} run return run function mgs:v5.0.0/multiplayer/editor/scope/primary_full
execute if data storage mgs:temp editor{primary:"mp5"} run return run function mgs:v5.0.0/multiplayer/editor/scope/primary_full
execute if data storage mgs:temp editor{primary:"mp7"} run return run function mgs:v5.0.0/multiplayer/editor/scope/primary_full
execute if data storage mgs:temp editor{primary:"m249"} run return run function mgs:v5.0.0/multiplayer/editor/scope/primary_no4
execute if data storage mgs:temp editor{primary:"rpk"} run return run function mgs:v5.0.0/multiplayer/editor/scope/primary_full
execute if data storage mgs:temp editor{primary:"svd"} run return run function mgs:v5.0.0/multiplayer/editor/scope/primary_full
execute if data storage mgs:temp editor{primary:"m82"} run return run function mgs:v5.0.0/multiplayer/editor/scope/primary_full
execute if data storage mgs:temp editor{primary:"mosin"} run return run function mgs:v5.0.0/multiplayer/editor/scope/primary_1only
execute if data storage mgs:temp editor{primary:"m24"} run return run function mgs:v5.0.0/multiplayer/editor/scope/primary_full
execute if data storage mgs:temp editor{primary:"spas12"} run return run function mgs:v5.0.0/multiplayer/editor/scope/primary_no4
execute if data storage mgs:temp editor{primary:"m500"} run return run function mgs:v5.0.0/multiplayer/editor/scope/primary_no4
execute if data storage mgs:temp editor{primary:"m590"} run return run function mgs:v5.0.0/multiplayer/editor/scope/primary_no4

# No scope variants: go directly to secondary selection
function mgs:v5.0.0/multiplayer/editor/show_secondary_dialog

