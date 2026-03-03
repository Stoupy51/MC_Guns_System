
#> mgs:v5.0.0/multiplayer/editor/pick_equipment
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Store equipment preset choice
execute if score @s mgs.player.config matches 300 run data modify storage mgs:temp editor.equipment_idx set value 0
execute if score @s mgs.player.config matches 300 run data modify storage mgs:temp editor.equipment_name set value "2x Frag Grenade"
execute if score @s mgs.player.config matches 301 run data modify storage mgs:temp editor.equipment_idx set value 1
execute if score @s mgs.player.config matches 301 run data modify storage mgs:temp editor.equipment_name set value "2x Semtex"
execute if score @s mgs.player.config matches 302 run data modify storage mgs:temp editor.equipment_idx set value 2
execute if score @s mgs.player.config matches 302 run data modify storage mgs:temp editor.equipment_name set value "2x Flash Grenade"
execute if score @s mgs.player.config matches 303 run data modify storage mgs:temp editor.equipment_idx set value 3
execute if score @s mgs.player.config matches 303 run data modify storage mgs:temp editor.equipment_name set value "2x Smoke Grenade"
execute if score @s mgs.player.config matches 304 run data modify storage mgs:temp editor.equipment_idx set value 4
execute if score @s mgs.player.config matches 304 run data modify storage mgs:temp editor.equipment_name set value "Frag + Flash"
execute if score @s mgs.player.config matches 305 run data modify storage mgs:temp editor.equipment_idx set value 5
execute if score @s mgs.player.config matches 305 run data modify storage mgs:temp editor.equipment_name set value "Frag + Smoke"
execute if score @s mgs.player.config matches 306 run data modify storage mgs:temp editor.equipment_idx set value 6
execute if score @s mgs.player.config matches 306 run data modify storage mgs:temp editor.equipment_name set value "Semtex + Flash"
execute if score @s mgs.player.config matches 307 run data modify storage mgs:temp editor.equipment_idx set value 7
execute if score @s mgs.player.config matches 307 run data modify storage mgs:temp editor.equipment_name set value "Semtex + Smoke"
execute if score @s mgs.player.config matches 308 run data modify storage mgs:temp editor.equipment_idx set value 8
execute if score @s mgs.player.config matches 308 run data modify storage mgs:temp editor.equipment_name set value "Flash + Smoke"
execute if score @s mgs.player.config matches 309 run data modify storage mgs:temp editor.equipment_idx set value 9
execute if score @s mgs.player.config matches 309 run data modify storage mgs:temp editor.equipment_name set value "No Equipment"

# Advance to step 4
scoreboard players set @s mgs.mp.edit_step 4

# Build confirmation dialog with summary
# We use a notice-style dialog with two action buttons (public/private)
data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate: "mgs.create_loadout_confirm",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:{translate: "mgs.review_your_loadout",color:"white"}},{type:"minecraft:item",item:{id:"minecraft:poisonous_potato",components:{"minecraft:item_model":"mgs:placeholder"}},description:{contents:[{"translate": "mgs.loading","color":"gray"}]}}],actions:[{label:{translate: "mgs.save_as_public",color:"green"},tooltip:{translate: "mgs.everyone_can_see_and_use_this_loadout"},action:{type:"run_command",command:"/trigger mgs.player.config set 350"}},{label:{translate: "mgs.save_as_private",color:"yellow"},tooltip:{translate: "mgs.only_you_can_see_and_use_this_loadout"},action:{type:"run_command",command:"/trigger mgs.player.config set 351"}}],columns:2,after_action:"close",exit_action:{label:"Cancel"}}

# Show dialog via macro-built summary
function mgs:v5.0.0/multiplayer/editor/show_confirm with storage mgs:temp editor

