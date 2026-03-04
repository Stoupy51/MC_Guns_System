
#> mgs:v5.0.0/multiplayer/editor/save
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Determine visibility from trigger value
scoreboard players set #cl_public mgs.data 0
execute if score @s mgs.player.config matches 350 run scoreboard players set #cl_public mgs.data 1

# Initialize build workspace
data modify storage mgs:temp _build set value {}

# Look up primary weapon slot data
execute if data storage mgs:temp editor{primary:"ak47"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[0]
execute if data storage mgs:temp editor{primary:"m16a4"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[1]
execute if data storage mgs:temp editor{primary:"famas"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[2]
execute if data storage mgs:temp editor{primary:"aug"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[3]
execute if data storage mgs:temp editor{primary:"m4a1"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[4]
execute if data storage mgs:temp editor{primary:"fnfal"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[5]
execute if data storage mgs:temp editor{primary:"g3a3"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[6]
execute if data storage mgs:temp editor{primary:"scar17"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[7]
execute if data storage mgs:temp editor{primary:"mp5"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[8]
execute if data storage mgs:temp editor{primary:"mp7"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[9]
execute if data storage mgs:temp editor{primary:"mac10"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[10]
execute if data storage mgs:temp editor{primary:"ppsh41"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[11]
execute if data storage mgs:temp editor{primary:"sten"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[12]
execute if data storage mgs:temp editor{primary:"m249"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[13]
execute if data storage mgs:temp editor{primary:"rpk"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[14]
execute if data storage mgs:temp editor{primary:"svd"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[15]
execute if data storage mgs:temp editor{primary:"m82"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[16]
execute if data storage mgs:temp editor{primary:"mosin"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[17]
execute if data storage mgs:temp editor{primary:"m24"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[18]
execute if data storage mgs:temp editor{primary:"spas12"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[19]
execute if data storage mgs:temp editor{primary:"m500"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[20]
execute if data storage mgs:temp editor{primary:"m590"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[21]
execute if data storage mgs:temp editor{primary:"rpg7"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[22]

# Look up secondary weapon slot data
execute if data storage mgs:temp editor{secondary:"m1911"} run data modify storage mgs:temp _build.secondary_data set from storage mgs:multiplayer secondary_slot_table[0]
execute if data storage mgs:temp editor{secondary:"m9"} run data modify storage mgs:temp _build.secondary_data set from storage mgs:multiplayer secondary_slot_table[1]
execute if data storage mgs:temp editor{secondary:"deagle"} run data modify storage mgs:temp _build.secondary_data set from storage mgs:multiplayer secondary_slot_table[2]
execute if data storage mgs:temp editor{secondary:"makarov"} run data modify storage mgs:temp _build.secondary_data set from storage mgs:multiplayer secondary_slot_table[3]
execute if data storage mgs:temp editor{secondary:"glock17"} run data modify storage mgs:temp _build.secondary_data set from storage mgs:multiplayer secondary_slot_table[4]
execute if data storage mgs:temp editor{secondary:"glock18"} run data modify storage mgs:temp _build.secondary_data set from storage mgs:multiplayer secondary_slot_table[5]
execute if data storage mgs:temp editor{secondary:"vz61"} run data modify storage mgs:temp _build.secondary_data set from storage mgs:multiplayer secondary_slot_table[6]
execute if data storage mgs:temp editor{secondary:"ray_gun"} run data modify storage mgs:temp _build.secondary_data set from storage mgs:multiplayer secondary_slot_table[7]

# Build the new loadout entry (include new Pick-10 fields)
	data modify storage mgs:temp _new_loadout set value {id:0,owner_pid:0,owner_name:"",name:"",public:0b,likes:0,favorites_count:0,points_used:0,main_gun:"",main_gun_display:"",secondary_gun:"",secondary_gun_display:"None",primary_mag_count:1,secondary_mag_count:0,equip_slot1:"",equip_slot1_name:"None",equip_slot2:"",equip_slot2_name:"None",perks:[],slots:[]}
# Set loadout ID from counter
execute store result storage mgs:temp _new_loadout.id int 1 run data get storage mgs:multiplayer next_loadout_id

# Increment the counter
execute store result score #temp mgs.data run data get storage mgs:multiplayer next_loadout_id
scoreboard players add #temp mgs.data 1
execute store result storage mgs:multiplayer next_loadout_id int 1 run scoreboard players get #temp mgs.data

# Set owner info
execute store result storage mgs:temp _new_loadout.owner_pid int 1 run scoreboard players get @s mgs.mp.pid

# Capture owner username via player head loot table trick
tag @s add mgs.username_getter
execute at @s summon item_display run function mgs:v5.0.0/multiplayer/get_username
tag @s remove mgs.username_getter

# Set weapon IDs (scope-modified)
data modify storage mgs:temp _new_loadout.main_gun set from storage mgs:temp editor.primary_full
data modify storage mgs:temp _new_loadout.secondary_gun set from storage mgs:temp editor.secondary_full

# Copy Pick-10 fields from editor
data modify storage mgs:temp _new_loadout.primary_mag_count set from storage mgs:temp editor.primary_mag_count
data modify storage mgs:temp _new_loadout.secondary_mag_count set from storage mgs:temp editor.secondary_mag_count
data modify storage mgs:temp _new_loadout.equip_slot1 set from storage mgs:temp editor.equip_slot1
data modify storage mgs:temp _new_loadout.equip_slot2 set from storage mgs:temp editor.equip_slot2
data modify storage mgs:temp _new_loadout.perks set from storage mgs:temp editor.perks

# Compute points used = PICK10_TOTAL - remaining
scoreboard players set #pts_used mgs.data 10
scoreboard players operation #pts_used mgs.data -= @s mgs.mp.edit_points
execute store result storage mgs:temp _new_loadout.points_used int 1 run scoreboard players get #pts_used mgs.data

# Set equip slot display names
execute if data storage mgs:temp editor{equip_slot1:""} run data modify storage mgs:temp _new_loadout.equip_slot1_name set value "None"
execute if data storage mgs:temp editor{equip_slot1:"frag_grenade"} run data modify storage mgs:temp _new_loadout.equip_slot1_name set value "Frag Grenade"
execute if data storage mgs:temp editor{equip_slot1:"semtex"} run data modify storage mgs:temp _new_loadout.equip_slot1_name set value "Semtex"
execute if data storage mgs:temp editor{equip_slot1:"flash_grenade"} run data modify storage mgs:temp _new_loadout.equip_slot1_name set value "Flash"
execute if data storage mgs:temp editor{equip_slot1:"smoke_grenade"} run data modify storage mgs:temp _new_loadout.equip_slot1_name set value "Smoke"
execute if data storage mgs:temp editor{equip_slot2:""} run data modify storage mgs:temp _new_loadout.equip_slot2_name set value "None"
execute if data storage mgs:temp editor{equip_slot2:"frag_grenade"} run data modify storage mgs:temp _new_loadout.equip_slot2_name set value "Frag Grenade"
execute if data storage mgs:temp editor{equip_slot2:"semtex"} run data modify storage mgs:temp _new_loadout.equip_slot2_name set value "Semtex"
execute if data storage mgs:temp editor{equip_slot2:"flash_grenade"} run data modify storage mgs:temp _new_loadout.equip_slot2_name set value "Flash"
execute if data storage mgs:temp editor{equip_slot2:"smoke_grenade"} run data modify storage mgs:temp _new_loadout.equip_slot2_name set value "Smoke"

# Set visibility
execute if score #cl_public mgs.data matches 1 run data modify storage mgs:temp _new_loadout.public set value 1b

# Override weapon loot entries with scope-modified IDs
function mgs:v5.0.0/multiplayer/editor/fix_primary_loot with storage mgs:temp editor
execute if data storage mgs:temp _build.secondary_data run function mgs:v5.0.0/multiplayer/editor/fix_secondary_loot with storage mgs:temp editor

# Build slot list
# 1. Primary weapon (hotbar.0)
data modify storage mgs:temp _new_loadout.slots append from storage mgs:temp _build.primary_data.gun_slot

# 2. Secondary weapon (hotbar.1) — if selected
execute if data storage mgs:temp _build.secondary_data run data modify storage mgs:temp _new_loadout.slots append from storage mgs:temp _build.secondary_data.gun_slot

# 3. Equipment slots (hotbar.8 and hotbar.7)
execute unless data storage mgs:temp editor{equip_slot1:""} run function mgs:v5.0.0/multiplayer/editor/append_equip1 with storage mgs:temp editor
execute unless data storage mgs:temp editor{equip_slot2:""} run function mgs:v5.0.0/multiplayer/editor/append_equip2 with storage mgs:temp editor

# 4. Primary magazine slots (inventory slots starting at 0)
scoreboard players set #inv_slot mgs.data 0
data modify storage mgs:temp _mag_data set from storage mgs:temp _build.primary_data
execute store result score #pmag_count mgs.data run data get storage mgs:temp editor.primary_mag_count
execute if score #pmag_count mgs.data matches 1.. run function mgs:v5.0.0/multiplayer/editor/append_mag_slots

# 5. Secondary magazine slots (continuing from #inv_slot)
execute if data storage mgs:temp _build.secondary_data run function mgs:v5.0.0/multiplayer/editor/start_secondary_mags

# Auto-name the loadout and set gun display names
function mgs:v5.0.0/multiplayer/editor/set_name with storage mgs:temp editor
function mgs:v5.0.0/multiplayer/editor/set_main_gun_display with storage mgs:temp editor
data modify storage mgs:temp _new_loadout.secondary_gun_display set value "None"
execute unless data storage mgs:temp editor{secondary:""} run function mgs:v5.0.0/multiplayer/editor/set_sec_gun_display with storage mgs:temp editor

# Append to custom loadouts list
data modify storage mgs:multiplayer custom_loadouts append from storage mgs:temp _new_loadout

# Reset editor state
scoreboard players set @s mgs.mp.edit_step 0

# Notify player
function mgs:v5.0.0/multiplayer/editor/notify_saved with storage mgs:temp editor

