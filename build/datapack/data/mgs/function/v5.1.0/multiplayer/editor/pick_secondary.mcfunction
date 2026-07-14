
#> mgs:v5.1.0/multiplayer/editor/pick_secondary
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#

# Snapshot, apply the gun (scope/camo reset, 0 magazines), then commit against the budget
data modify storage mgs:temp _ed_bak set from storage mgs:temp editor
execute if score @s mgs.player.config matches 250 run data modify storage mgs:temp editor merge value {secondary:"m1911",secondary_name:"M1911",secondary_mag:"m1911_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"m1911"}
execute if score @s mgs.player.config matches 251 run data modify storage mgs:temp editor merge value {secondary:"m9",secondary_name:"M9",secondary_mag:"m9_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"m9"}
execute if score @s mgs.player.config matches 252 run data modify storage mgs:temp editor merge value {secondary:"deagle",secondary_name:"Deagle",secondary_mag:"deagle_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"deagle"}
execute if score @s mgs.player.config matches 253 run data modify storage mgs:temp editor merge value {secondary:"makarov",secondary_name:"Makarov",secondary_mag:"makarov_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"makarov"}
execute if score @s mgs.player.config matches 254 run data modify storage mgs:temp editor merge value {secondary:"glock17",secondary_name:"Glock 17",secondary_mag:"glock17_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"glock17"}
execute if score @s mgs.player.config matches 255 run data modify storage mgs:temp editor merge value {secondary:"glock18",secondary_name:"Glock 18",secondary_mag:"glock18_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"glock18"}
execute if score @s mgs.player.config matches 256 run data modify storage mgs:temp editor merge value {secondary:"vz61",secondary_name:"VZ-61",secondary_mag:"vz61_mag",secondary_mag_count:0,secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"vz61"}

execute store success score #ed_ok mgs.data run function mgs:v5.1.0/multiplayer/editor/commit_check
execute if score #ed_ok mgs.data matches 0 run return run function mgs:v5.1.0/multiplayer/editor/hub

# Continue: scope dialog for guns with variants, camo otherwise
execute if data storage mgs:temp editor{secondary:"deagle"} run return run function mgs:v5.1.0/multiplayer/editor/scope/secondary_4only

function mgs:v5.1.0/multiplayer/editor/show_secondary_camo_dialog

