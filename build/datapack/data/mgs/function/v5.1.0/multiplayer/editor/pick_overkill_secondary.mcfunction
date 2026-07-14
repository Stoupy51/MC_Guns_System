
#> mgs:v5.1.0/multiplayer/editor/pick_overkill_secondary
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#

# Snapshot, store the chosen primary as the secondary (0 magazines), commit against the budget
data modify storage mgs:temp _ed_bak set from storage mgs:temp editor
execute if score @s mgs.player.config matches 520 run data modify storage mgs:temp editor merge value {secondary:"ak47",secondary_name:"AK-47",secondary_mag:"ak47_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"ak47"}
execute if score @s mgs.player.config matches 521 run data modify storage mgs:temp editor merge value {secondary:"m16a4",secondary_name:"M16A4",secondary_mag:"m16a4_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"m16a4"}
execute if score @s mgs.player.config matches 522 run data modify storage mgs:temp editor merge value {secondary:"famas",secondary_name:"FAMAS",secondary_mag:"famas_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"famas"}
execute if score @s mgs.player.config matches 523 run data modify storage mgs:temp editor merge value {secondary:"aug",secondary_name:"AUG",secondary_mag:"aug_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"aug"}
execute if score @s mgs.player.config matches 524 run data modify storage mgs:temp editor merge value {secondary:"m4a1",secondary_name:"M4A1",secondary_mag:"m4a1_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"m4a1"}
execute if score @s mgs.player.config matches 525 run data modify storage mgs:temp editor merge value {secondary:"fnfal",secondary_name:"FN FAL",secondary_mag:"fnfal_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"fnfal"}
execute if score @s mgs.player.config matches 526 run data modify storage mgs:temp editor merge value {secondary:"g3a3",secondary_name:"G3A3",secondary_mag:"g3a3_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"g3a3"}
execute if score @s mgs.player.config matches 527 run data modify storage mgs:temp editor merge value {secondary:"scar17",secondary_name:"SCAR-17",secondary_mag:"scar17_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"scar17"}
execute if score @s mgs.player.config matches 528 run data modify storage mgs:temp editor merge value {secondary:"mp5",secondary_name:"MP5",secondary_mag:"mp5_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"mp5"}
execute if score @s mgs.player.config matches 529 run data modify storage mgs:temp editor merge value {secondary:"mp7",secondary_name:"MP7",secondary_mag:"mp7_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"mp7"}
execute if score @s mgs.player.config matches 530 run data modify storage mgs:temp editor merge value {secondary:"mac10",secondary_name:"MAC-10",secondary_mag:"mac10_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"mac10"}
execute if score @s mgs.player.config matches 531 run data modify storage mgs:temp editor merge value {secondary:"ppsh41",secondary_name:"PPSh-41",secondary_mag:"ppsh41_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"ppsh41"}
execute if score @s mgs.player.config matches 532 run data modify storage mgs:temp editor merge value {secondary:"sten",secondary_name:"Sten",secondary_mag:"sten_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"sten"}
execute if score @s mgs.player.config matches 533 run data modify storage mgs:temp editor merge value {secondary:"m249",secondary_name:"M249",secondary_mag:"m249_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"m249"}
execute if score @s mgs.player.config matches 534 run data modify storage mgs:temp editor merge value {secondary:"rpk",secondary_name:"RPK",secondary_mag:"rpk_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"rpk"}
execute if score @s mgs.player.config matches 535 run data modify storage mgs:temp editor merge value {secondary:"svd",secondary_name:"SVD",secondary_mag:"svd_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"svd"}
execute if score @s mgs.player.config matches 536 run data modify storage mgs:temp editor merge value {secondary:"m82",secondary_name:"M82",secondary_mag:"m82_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"m82"}
execute if score @s mgs.player.config matches 537 run data modify storage mgs:temp editor merge value {secondary:"mosin",secondary_name:"Mosin-Nagant",secondary_mag:"mosin_bullet",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"mosin"}
execute if score @s mgs.player.config matches 538 run data modify storage mgs:temp editor merge value {secondary:"m24",secondary_name:"M24",secondary_mag:"m24_bullet",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"m24"}
execute if score @s mgs.player.config matches 539 run data modify storage mgs:temp editor merge value {secondary:"spas12",secondary_name:"SPAS-12",secondary_mag:"spas12_shell",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"spas12"}
execute if score @s mgs.player.config matches 540 run data modify storage mgs:temp editor merge value {secondary:"m500",secondary_name:"M500",secondary_mag:"m500_shell",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"m500"}
execute if score @s mgs.player.config matches 541 run data modify storage mgs:temp editor merge value {secondary:"m590",secondary_name:"M590",secondary_mag:"m590_shell",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"m590"}
execute if score @s mgs.player.config matches 542 run data modify storage mgs:temp editor merge value {secondary:"rpg7",secondary_name:"RPG-7",secondary_mag:"rpg7_rocket",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"rpg7"}

execute store success score #ed_ok mgs.data run function mgs:v5.1.0/multiplayer/editor/commit_check
execute if score #ed_ok mgs.data matches 0 run return run function mgs:v5.1.0/multiplayer/editor/hub

# Overkill secondaries keep iron sights; go straight to camo
function mgs:v5.1.0/multiplayer/editor/show_secondary_camo_dialog

