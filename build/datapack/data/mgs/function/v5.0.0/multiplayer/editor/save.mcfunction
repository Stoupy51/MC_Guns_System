
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
execute if data storage mgs:temp editor{primary:"m24_4"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[18]
execute if data storage mgs:temp editor{primary:"spas12"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[19]
execute if data storage mgs:temp editor{primary:"m500"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[20]
execute if data storage mgs:temp editor{primary:"m590"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[21]
execute if data storage mgs:temp editor{primary:"rpg7"} run data modify storage mgs:temp _build.primary_data set from storage mgs:multiplayer primary_slot_table[22]

# Look up secondary weapon slot data (skip if no secondary)
execute if data storage mgs:temp editor{secondary:"m1911"} run data modify storage mgs:temp _build.secondary_data set from storage mgs:multiplayer secondary_slot_table[0]
execute if data storage mgs:temp editor{secondary:"m9"} run data modify storage mgs:temp _build.secondary_data set from storage mgs:multiplayer secondary_slot_table[1]
execute if data storage mgs:temp editor{secondary:"deagle"} run data modify storage mgs:temp _build.secondary_data set from storage mgs:multiplayer secondary_slot_table[2]
execute if data storage mgs:temp editor{secondary:"makarov"} run data modify storage mgs:temp _build.secondary_data set from storage mgs:multiplayer secondary_slot_table[3]
execute if data storage mgs:temp editor{secondary:"glock17"} run data modify storage mgs:temp _build.secondary_data set from storage mgs:multiplayer secondary_slot_table[4]
execute if data storage mgs:temp editor{secondary:"glock18"} run data modify storage mgs:temp _build.secondary_data set from storage mgs:multiplayer secondary_slot_table[5]
execute if data storage mgs:temp editor{secondary:"vz61"} run data modify storage mgs:temp _build.secondary_data set from storage mgs:multiplayer secondary_slot_table[6]

# Look up equipment slot data
execute if data storage mgs:temp editor{equipment_idx:0} run data modify storage mgs:temp _build.equipment_data set from storage mgs:multiplayer equipment_slot_table[0]
execute if data storage mgs:temp editor{equipment_idx:1} run data modify storage mgs:temp _build.equipment_data set from storage mgs:multiplayer equipment_slot_table[1]
execute if data storage mgs:temp editor{equipment_idx:2} run data modify storage mgs:temp _build.equipment_data set from storage mgs:multiplayer equipment_slot_table[2]
execute if data storage mgs:temp editor{equipment_idx:3} run data modify storage mgs:temp _build.equipment_data set from storage mgs:multiplayer equipment_slot_table[3]
execute if data storage mgs:temp editor{equipment_idx:4} run data modify storage mgs:temp _build.equipment_data set from storage mgs:multiplayer equipment_slot_table[4]
execute if data storage mgs:temp editor{equipment_idx:5} run data modify storage mgs:temp _build.equipment_data set from storage mgs:multiplayer equipment_slot_table[5]
execute if data storage mgs:temp editor{equipment_idx:6} run data modify storage mgs:temp _build.equipment_data set from storage mgs:multiplayer equipment_slot_table[6]
execute if data storage mgs:temp editor{equipment_idx:7} run data modify storage mgs:temp _build.equipment_data set from storage mgs:multiplayer equipment_slot_table[7]
execute if data storage mgs:temp editor{equipment_idx:8} run data modify storage mgs:temp _build.equipment_data set from storage mgs:multiplayer equipment_slot_table[8]
execute if data storage mgs:temp editor{equipment_idx:9} run data modify storage mgs:temp _build.equipment_data set from storage mgs:multiplayer equipment_slot_table[9]

# Build the final loadout entry
# Start with base structure
data modify storage mgs:temp _new_loadout set value {id:0,owner_pid:0,owner_name:"",name:"",public:0b,likes:0,main_gun:"",secondary_gun:"",slots:[]}

# Set loadout ID from counter
execute store result storage mgs:temp _new_loadout.id int 1 run data get storage mgs:multiplayer next_loadout_id

# Increment the counter
execute store result score #temp mgs.data run data get storage mgs:multiplayer next_loadout_id
scoreboard players add #temp mgs.data 1
execute store result storage mgs:multiplayer next_loadout_id int 1 run scoreboard players get #temp mgs.data

# Set owner info
execute store result storage mgs:temp _new_loadout.owner_pid int 1 run scoreboard players get @s mgs.mp.pid
# Owner name is set by a macro call (pass player display name via team prefix trick)

# Set weapon info
data modify storage mgs:temp _new_loadout.main_gun set from storage mgs:temp editor.primary
data modify storage mgs:temp _new_loadout.secondary_gun set from storage mgs:temp editor.secondary

# Set visibility
execute if score #cl_public mgs.data matches 1 run data modify storage mgs:temp _new_loadout.public set value 1b

# Build the combined slot list: primary slots + secondary slots + equipment slots
# 1. Copy primary weapon & magazine slots
data modify storage mgs:temp _new_loadout.slots set from storage mgs:temp _build.primary_data.slots

# 2. Append secondary gun slot (hotbar.1)
execute if data storage mgs:temp _build.secondary_data run data modify storage mgs:temp _new_loadout.slots append from storage mgs:temp _build.secondary_data.fixed_slots[0]

# 3. Append secondary magazine slots (need to fix inventory slot numbers)
# Get next_inv_slot from primary data to know where secondary mags start
execute store result score #inv_slot mgs.data run data get storage mgs:temp _build.primary_data.next_inv_slot
# Use recursive function to append secondary mags with correct slot numbers
execute if data storage mgs:temp _build.secondary_data.mag_slots[0] run function mgs:v5.0.0/multiplayer/editor/append_sec_mags

# 4. Append equipment slots
execute if data storage mgs:temp _build.equipment_data.slots[0] run function mgs:v5.0.0/multiplayer/editor/append_equip_slots

# Auto-generate loadout name: "Primary + Secondary" or just "Primary"
function mgs:v5.0.0/multiplayer/editor/set_name with storage mgs:temp editor

# Append to the custom loadouts list
data modify storage mgs:multiplayer custom_loadouts append from storage mgs:temp _new_loadout

# Reset editor state
scoreboard players set @s mgs.mp.edit_step 0

# Notify player
function mgs:v5.0.0/multiplayer/editor/notify_saved with storage mgs:temp editor

