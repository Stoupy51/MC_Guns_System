
#> mgs:v5.0.0/multiplayer/editor/pick_secondary
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Store secondary weapon choice based on trigger value
execute if score @s mgs.player.config matches 250 run data modify storage mgs:temp editor.secondary set value "m1911"
execute if score @s mgs.player.config matches 250 run data modify storage mgs:temp editor.secondary_name set value "M1911"
execute if score @s mgs.player.config matches 250 run data modify storage mgs:temp editor.secondary_mag set value "m1911_mag"
execute if score @s mgs.player.config matches 250 run data modify storage mgs:temp editor.secondary_mag_count set value 2
execute if score @s mgs.player.config matches 251 run data modify storage mgs:temp editor.secondary set value "m9"
execute if score @s mgs.player.config matches 251 run data modify storage mgs:temp editor.secondary_name set value "M9"
execute if score @s mgs.player.config matches 251 run data modify storage mgs:temp editor.secondary_mag set value "m9_mag"
execute if score @s mgs.player.config matches 251 run data modify storage mgs:temp editor.secondary_mag_count set value 2
execute if score @s mgs.player.config matches 252 run data modify storage mgs:temp editor.secondary set value "deagle"
execute if score @s mgs.player.config matches 252 run data modify storage mgs:temp editor.secondary_name set value "Deagle"
execute if score @s mgs.player.config matches 252 run data modify storage mgs:temp editor.secondary_mag set value "deagle_mag"
execute if score @s mgs.player.config matches 252 run data modify storage mgs:temp editor.secondary_mag_count set value 2
execute if score @s mgs.player.config matches 253 run data modify storage mgs:temp editor.secondary set value "makarov"
execute if score @s mgs.player.config matches 253 run data modify storage mgs:temp editor.secondary_name set value "Makarov"
execute if score @s mgs.player.config matches 253 run data modify storage mgs:temp editor.secondary_mag set value "makarov_mag"
execute if score @s mgs.player.config matches 253 run data modify storage mgs:temp editor.secondary_mag_count set value 2
execute if score @s mgs.player.config matches 254 run data modify storage mgs:temp editor.secondary set value "glock17"
execute if score @s mgs.player.config matches 254 run data modify storage mgs:temp editor.secondary_name set value "Glock 17"
execute if score @s mgs.player.config matches 254 run data modify storage mgs:temp editor.secondary_mag set value "glock17_mag"
execute if score @s mgs.player.config matches 254 run data modify storage mgs:temp editor.secondary_mag_count set value 2
execute if score @s mgs.player.config matches 255 run data modify storage mgs:temp editor.secondary set value "glock18"
execute if score @s mgs.player.config matches 255 run data modify storage mgs:temp editor.secondary_name set value "Glock 18"
execute if score @s mgs.player.config matches 255 run data modify storage mgs:temp editor.secondary_mag set value "glock18_mag"
execute if score @s mgs.player.config matches 255 run data modify storage mgs:temp editor.secondary_mag_count set value 2
execute if score @s mgs.player.config matches 256 run data modify storage mgs:temp editor.secondary set value "vz61"
execute if score @s mgs.player.config matches 256 run data modify storage mgs:temp editor.secondary_name set value "VZ-61"
execute if score @s mgs.player.config matches 256 run data modify storage mgs:temp editor.secondary_mag set value "vz61_mag"
execute if score @s mgs.player.config matches 256 run data modify storage mgs:temp editor.secondary_mag_count set value 2
execute if score @s mgs.player.config matches 258 run data modify storage mgs:temp editor.secondary set value ""
execute if score @s mgs.player.config matches 258 run data modify storage mgs:temp editor.secondary_name set value "None"

# Advance to step 3
scoreboard players set @s mgs.mp.edit_step 3

# Build equipment preset selection dialog
data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate: "mgs.create_loadout_pick_equipment",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:{translate: "mgs.choose_your_equipment_loadout",color:"gray"}}],actions:[{label:{translate: "mgs.2x_frag_grenade",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 300"}},{label:{translate: "mgs.2x_semtex",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 301"}},{label:{translate: "mgs.2x_flash_grenade",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 302"}},{label:{translate: "mgs.2x_smoke_grenade",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 303"}},{label:{translate: "mgs.frag_flash",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 304"}},{label:{translate: "mgs.frag_smoke",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 305"}},{label:{translate: "mgs.semtex_flash",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 306"}},{label:{translate: "mgs.semtex_smoke",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 307"}},{label:{translate: "mgs.flash_smoke",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 308"}},{label:{translate: "mgs.no_equipment",color:"green"},action:{type:"run_command",command:"/trigger mgs.player.config set 309"}}],columns:2,after_action:"close",exit_action:{label:"Cancel"}}

# Show dialog
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

