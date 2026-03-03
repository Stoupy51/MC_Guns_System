
#> mgs:v5.0.0/multiplayer/editor/pick_primary
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Store primary weapon choice based on trigger value
execute if score @s mgs.player.config matches 200 run data modify storage mgs:temp editor set value {primary:"ak47",primary_name:"AK-47",primary_mag:"ak47_mag",primary_mag_count:3}
execute if score @s mgs.player.config matches 201 run data modify storage mgs:temp editor set value {primary:"m16a4",primary_name:"M16A4",primary_mag:"m16a4_mag",primary_mag_count:3}
execute if score @s mgs.player.config matches 202 run data modify storage mgs:temp editor set value {primary:"famas",primary_name:"FAMAS",primary_mag:"famas_mag",primary_mag_count:3}
execute if score @s mgs.player.config matches 203 run data modify storage mgs:temp editor set value {primary:"aug",primary_name:"AUG",primary_mag:"aug_mag",primary_mag_count:3}
execute if score @s mgs.player.config matches 204 run data modify storage mgs:temp editor set value {primary:"m4a1",primary_name:"M4A1",primary_mag:"m4a1_mag",primary_mag_count:3}
execute if score @s mgs.player.config matches 205 run data modify storage mgs:temp editor set value {primary:"fnfal",primary_name:"FN FAL",primary_mag:"fnfal_mag",primary_mag_count:3}
execute if score @s mgs.player.config matches 206 run data modify storage mgs:temp editor set value {primary:"g3a3",primary_name:"G3A3",primary_mag:"g3a3_mag",primary_mag_count:3}
execute if score @s mgs.player.config matches 207 run data modify storage mgs:temp editor set value {primary:"scar17",primary_name:"SCAR-17",primary_mag:"scar17_mag",primary_mag_count:3}
execute if score @s mgs.player.config matches 208 run data modify storage mgs:temp editor set value {primary:"mp5",primary_name:"MP5",primary_mag:"mp5_mag",primary_mag_count:4}
execute if score @s mgs.player.config matches 209 run data modify storage mgs:temp editor set value {primary:"mp7",primary_name:"MP7",primary_mag:"mp7_mag",primary_mag_count:4}
execute if score @s mgs.player.config matches 210 run data modify storage mgs:temp editor set value {primary:"mac10",primary_name:"MAC-10",primary_mag:"mac10_mag",primary_mag_count:4}
execute if score @s mgs.player.config matches 211 run data modify storage mgs:temp editor set value {primary:"ppsh41",primary_name:"PPSh-41",primary_mag:"ppsh41_mag",primary_mag_count:3}
execute if score @s mgs.player.config matches 212 run data modify storage mgs:temp editor set value {primary:"sten",primary_name:"Sten",primary_mag:"sten_mag",primary_mag_count:3}
execute if score @s mgs.player.config matches 213 run data modify storage mgs:temp editor set value {primary:"m249",primary_name:"M249",primary_mag:"m249_mag",primary_mag_count:3}
execute if score @s mgs.player.config matches 214 run data modify storage mgs:temp editor set value {primary:"rpk",primary_name:"RPK",primary_mag:"rpk_mag",primary_mag_count:3}
execute if score @s mgs.player.config matches 215 run data modify storage mgs:temp editor set value {primary:"svd",primary_name:"SVD",primary_mag:"svd_mag",primary_mag_count:3}
execute if score @s mgs.player.config matches 216 run data modify storage mgs:temp editor set value {primary:"m82",primary_name:"M82",primary_mag:"m82_mag",primary_mag_count:3}
execute if score @s mgs.player.config matches 217 run data modify storage mgs:temp editor set value {primary:"mosin",primary_name:"Mosin-Nagant",primary_mag:"mosin_bullet",primary_mag_count:10}
execute if score @s mgs.player.config matches 218 run data modify storage mgs:temp editor set value {primary:"m24_4",primary_name:"M24",primary_mag:"m24_bullet",primary_mag_count:10}
execute if score @s mgs.player.config matches 219 run data modify storage mgs:temp editor set value {primary:"spas12",primary_name:"SPAS-12",primary_mag:"spas12_shell",primary_mag_count:16}
execute if score @s mgs.player.config matches 220 run data modify storage mgs:temp editor set value {primary:"m500",primary_name:"M500",primary_mag:"m500_shell",primary_mag_count:12}
execute if score @s mgs.player.config matches 221 run data modify storage mgs:temp editor set value {primary:"m590",primary_name:"M590",primary_mag:"m590_shell",primary_mag_count:16}
execute if score @s mgs.player.config matches 222 run data modify storage mgs:temp editor set value {primary:"rpg7",primary_name:"RPG-7",primary_mag:"rpg7_rocket",primary_mag_count:3}

# Advance to step 2
scoreboard players set @s mgs.mp.edit_step 2

# Build secondary weapon selection dialog
data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate: "mgs.create_loadout_pick_secondary",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:{translate: "mgs.choose_your_secondary_weapon_or_skip",color:"gray"}}],actions:[{label:{translate: "mgs.m1911",color:"green"},tooltip:{translate: "mgs.pistol"},action:{type:"run_command",command:"/trigger mgs.player.config set 250"}},{label:{text:"M9",color:"green"},tooltip:{translate: "mgs.pistol"},action:{type:"run_command",command:"/trigger mgs.player.config set 251"}},{label:{translate: "mgs.deagle",color:"green"},tooltip:{translate: "mgs.pistol"},action:{type:"run_command",command:"/trigger mgs.player.config set 252"}},{label:{translate: "mgs.makarov",color:"green"},tooltip:{translate: "mgs.pistol"},action:{type:"run_command",command:"/trigger mgs.player.config set 253"}},{label:{translate: "mgs.glock_17",color:"green"},tooltip:{translate: "mgs.pistol"},action:{type:"run_command",command:"/trigger mgs.player.config set 254"}},{label:{translate: "mgs.glock_18",color:"green"},tooltip:{translate: "mgs.pistol"},action:{type:"run_command",command:"/trigger mgs.player.config set 255"}},{label:{translate: "mgs.vz_61",color:"green"},tooltip:{translate: "mgs.pistol"},action:{type:"run_command",command:"/trigger mgs.player.config set 256"}},{label:{translate: "mgs.no_secondary",color:"red"},tooltip:{translate: "mgs.skip_secondary_weapon"},action:{type:"run_command",command:"/trigger mgs.player.config set 258"}}],columns:2,after_action:"close",exit_action:{label:"Cancel"}}

# Show dialog
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

