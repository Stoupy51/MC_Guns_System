
#> mgs:v5.1.0/multiplayer/editor/hub
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#			mgs:v5.1.0/multiplayer/editor/start
#			mgs:v5.1.0/multiplayer/editor/pick_primary
#			mgs:v5.1.0/multiplayer/editor/pick_secondary
#			mgs:v5.1.0/multiplayer/editor/pick_overkill_secondary
#			mgs:v5.1.0/multiplayer/editor/remove_primary
#			mgs:v5.1.0/multiplayer/editor/remove_secondary
#			mgs:v5.1.0/multiplayer/editor/pick_primary_camo
#			mgs:v5.1.0/multiplayer/editor/pick_secondary_camo
#			mgs:v5.1.0/multiplayer/editor/pick_equip1_camo
#			mgs:v5.1.0/multiplayer/editor/pick_equip2_camo
#			mgs:v5.1.0/multiplayer/editor/show_primary_mags_dialog
#			mgs:v5.1.0/multiplayer/editor/show_secondary_mags_dialog
#			mgs:v5.1.0/multiplayer/editor/pick_primary_mags
#			mgs:v5.1.0/multiplayer/editor/pick_secondary_mags
#			mgs:v5.1.0/multiplayer/editor/pick_equip_slot1
#			mgs:v5.1.0/multiplayer/editor/pick_equip_slot2
#			mgs:v5.1.0/multiplayer/editor/save
#			mgs:v5.1.0/multiplayer/custom/edit
#

# Points summary
function mgs:v5.1.0/multiplayer/editor/recompute_points
scoreboard players set #pts_used mgs.data 10
scoreboard players operation #pts_used mgs.data -= @s mgs.mp.edit_points
execute store result storage mgs:temp _hub.pts int 1 run scoreboard players get @s mgs.mp.edit_points
execute store result storage mgs:temp _hub.used int 1 run scoreboard players get #pts_used mgs.data
execute store result storage mgs:temp _hub.perks int 1 run data get storage mgs:temp editor.perks

# Base dialog, then one row per category (labels show the current selection)
function mgs:v5.1.0/multiplayer/editor/hub_base with storage mgs:temp _hub
function mgs:v5.1.0/multiplayer/editor/hub_row_primary with storage mgs:temp editor
execute if data storage mgs:temp editor{primary:""} run data modify storage mgs:temp dialog.actions append value {label:{text:"\ud83d\udce6 Primary Mags \u2014 Unavailable",color:"dark_gray"},tooltip:{translate:"mgs.pick_a_primary_weapon_first",color:"red"},action:{type:"run_command",command:"/trigger mgs.player.config set 103"}}
execute unless data storage mgs:temp editor{primary:""} run function mgs:v5.1.0/multiplayer/editor/hub_row_primary_mags with storage mgs:temp editor
function mgs:v5.1.0/multiplayer/editor/hub_row_secondary with storage mgs:temp editor
execute if data storage mgs:temp editor{secondary:""} run data modify storage mgs:temp dialog.actions append value {label:{text:"\ud83d\udce6 Secondary Mags \u2014 Unavailable",color:"dark_gray"},tooltip:{translate:"mgs.pick_a_secondary_weapon_first",color:"red"},action:{type:"run_command",command:"/trigger mgs.player.config set 103"}}
execute unless data storage mgs:temp editor{secondary:""} run function mgs:v5.1.0/multiplayer/editor/hub_row_secondary_mags with storage mgs:temp editor
function mgs:v5.1.0/multiplayer/editor/hub_row_equip1 with storage mgs:temp editor
function mgs:v5.1.0/multiplayer/editor/hub_row_equip2 with storage mgs:temp editor
function mgs:v5.1.0/multiplayer/editor/hub_row_perks with storage mgs:temp _hub

# Save buttons (grayed out until a primary weapon is selected)
execute if data storage mgs:temp editor{primary:""} run data modify storage mgs:temp dialog.actions append value {label:{text:"\ud83d\udcbe Save \u2014 Unavailable",color:"dark_gray"},tooltip:{translate:"mgs.a_primary_weapon_is_required",color:"red"},action:{type:"run_command",command:"/trigger mgs.player.config set 103"}}
execute unless data storage mgs:temp editor{primary:""} run data modify storage mgs:temp dialog.actions append value {label:{text:"\ud83d\udcbe Save as Public",color:"green",bold:true},tooltip:{translate:"mgs.everyone_can_see_and_use_this_loadout"},action:{type:"run_command",command:"/trigger mgs.player.config set 350"}}
execute unless data storage mgs:temp editor{primary:""} run data modify storage mgs:temp dialog.actions append value {label:{text:"\ud83d\udcbe Save as Private",color:"yellow",bold:true},tooltip:{translate:"mgs.only_you_can_see_and_use_this_loadout"},action:{type:"run_command",command:"/trigger mgs.player.config set 351"}}

# Show
function mgs:v5.1.0/multiplayer/show_dialog with storage mgs:temp

