
#> mgs:v5.0.0/multiplayer/editor/show_confirm
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/perks_done with storage mgs:temp editor
#
# @args		primary_name (unknown)
#			primary_scope_name (unknown)
#			primary_mag_count (unknown)
#			secondary_name (unknown)
#			secondary_mag_count (unknown)
#			equip_slot1 (unknown)
#			equip_slot2 (unknown)
#

# Compute points used = PICK10_TOTAL - remaining
scoreboard players set #pts_used mgs.data 10
scoreboard players operation #pts_used mgs.data -= @s mgs.mp.edit_points
execute store result storage mgs:temp _pts_used int 1 run scoreboard players get #pts_used mgs.data

$data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate:"mgs.create_loadout_review",color:"gold",bold:true},body:[{type:"minecraft:plain_message",contents:["",["",{"translate":"mgs.points_used"},": "],{"translate":"mgs.placeholder","color":"gold"}]},{type:"minecraft:plain_message",contents:{translate:"mgs.review_your_loadout_before_saving",color:"white"}},{type:"minecraft:plain_message",contents:["","","➤ ",{"translate":"mgs.primary"},": ",{"text":"$(primary_name)","color":"green","bold":true},{"text":" ($(primary_scope_name)) x$(primary_mag_count) mags","color":"dark_green"}]},{type:"minecraft:plain_message",contents:["","","➤ ",{"translate":"mgs.secondary"},": ",{"text":"$(secondary_name)","color":"yellow","bold":true},{"text":" x$(secondary_mag_count) mags","color":"gold"}]},{type:"minecraft:plain_message",contents:["","","➤ ",[{"translate":"mgs.equip"}, " 1"],": ",{"text":"$(equip_slot1)","color":"aqua","bold":true}]},{type:"minecraft:plain_message",contents:["","","➤ ",[{"translate":"mgs.equip"}, " 2"],": ",{"text":"$(equip_slot2)","color":"aqua","bold":true}]}],actions:[{label:{translate:"mgs.save_as_public",color:"green"},tooltip:{translate:"mgs.everyone_can_see_and_use_this_loadout"},action:{type:"run_command",command:"/trigger mgs.player.config set 350"}},{label:{translate:"mgs.save_as_private",color:"yellow"},tooltip:{translate:"mgs.only_you_can_see_and_use_this_loadout"},action:{type:"run_command",command:"/trigger mgs.player.config set 351"}}],columns:2,after_action:"close",exit_action:{label:"Back",action:{type:"run_command",command:"/trigger mgs.player.config set 380"}}}

# Fix the pts used line (body[0])
function mgs:v5.0.0/multiplayer/editor/patch_pts_used with storage mgs:temp

# Append perk lines to body
execute if data storage mgs:temp editor.perks[0] run function mgs:v5.0.0/multiplayer/editor/append_perks_to_confirm

# Show
function mgs:v5.0.0/multiplayer/show_dialog with storage mgs:temp

