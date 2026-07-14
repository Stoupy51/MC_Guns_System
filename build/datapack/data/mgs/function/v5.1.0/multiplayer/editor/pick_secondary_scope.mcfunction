
#> mgs:v5.1.0/multiplayer/editor/pick_secondary_scope
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#

data modify storage mgs:temp _ed_bak set from storage mgs:temp editor
execute if score @s mgs.player.config matches 260 run data modify storage mgs:temp editor merge value {secondary_scope:"",secondary_scope_name:"Iron Sights"}
execute if score @s mgs.player.config matches 261 run data modify storage mgs:temp editor merge value {secondary_scope:"_1",secondary_scope_name:"Holographic"}
execute if score @s mgs.player.config matches 262 run data modify storage mgs:temp editor merge value {secondary_scope:"_2",secondary_scope_name:"Kobra"}
execute if score @s mgs.player.config matches 263 run data modify storage mgs:temp editor merge value {secondary_scope:"_3",secondary_scope_name:"ACOG Red Dot (3x Scope)"}
execute if score @s mgs.player.config matches 264 run data modify storage mgs:temp editor merge value {secondary_scope:"_4",secondary_scope_name:"Mk4 (4x Scope)"}

execute store success score #ed_ok mgs.data run function mgs:v5.1.0/multiplayer/editor/commit_check

# Continue to camo either way (a denied scope simply stays on iron sights)
function mgs:v5.1.0/multiplayer/editor/show_secondary_camo_dialog

