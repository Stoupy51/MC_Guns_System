
#> mgs:v5.3.0/multiplayer/editor/pick_primary_scope
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/player/config/process
#

data modify storage mgs:temp _ed_bak set from storage mgs:temp editor
execute if score @s mgs.player.config matches 230 run data modify storage mgs:temp editor merge value {primary_scope:"",primary_scope_name:"Iron Sights"}
execute if score @s mgs.player.config matches 231 run data modify storage mgs:temp editor merge value {primary_scope:"_1",primary_scope_name:"Holographic"}
execute if score @s mgs.player.config matches 232 run data modify storage mgs:temp editor merge value {primary_scope:"_2",primary_scope_name:"Kobra"}
execute if score @s mgs.player.config matches 233 run data modify storage mgs:temp editor merge value {primary_scope:"_3",primary_scope_name:"ACOG Red Dot (3x Scope)"}
execute if score @s mgs.player.config matches 234 run data modify storage mgs:temp editor merge value {primary_scope:"_4",primary_scope_name:"Mk4 (4x Scope)"}

execute if data storage mgs:temp editor{primary:"mosin",primary_scope:"_1"} run data modify storage mgs:temp editor.primary_scope_name set value "PU Scope (4x)"
execute if data storage mgs:temp editor{primary:"ak47",primary_scope:"_4"} run data modify storage mgs:temp editor.primary_scope_name set value "PSO (4x Scope)"
execute if data storage mgs:temp editor{primary:"svd",primary_scope:"_4"} run data modify storage mgs:temp editor.primary_scope_name set value "PSO (4x Scope)"
execute if data storage mgs:temp editor{primary:"rpk",primary_scope:"_4"} run data modify storage mgs:temp editor.primary_scope_name set value "PSO (4x Scope)"
execute store success score #ed_ok mgs.data run function mgs:v5.3.0/multiplayer/editor/commit_check

# A denied scope stays on iron sights; camo follows either way.
function mgs:v5.3.0/multiplayer/editor/show_primary_camo_dialog

