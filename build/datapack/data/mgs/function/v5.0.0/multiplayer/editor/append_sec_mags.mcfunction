
#> mgs:v5.0.0/multiplayer/editor/append_sec_mags
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/save
#			mgs:v5.0.0/multiplayer/editor/append_sec_mags
#

# Copy the first mag slot template
data modify storage mgs:temp _sec_mag set from storage mgs:temp _build.secondary_data.mag_slots[0]

# Set the correct inventory slot number using score
# Build the slot string: "inventory.N"
execute store result storage mgs:temp _inv_n int 1 run scoreboard players get #inv_slot mgs.data
function mgs:v5.0.0/multiplayer/editor/set_sec_mag_slot with storage mgs:temp

# Append to loadout slots
data modify storage mgs:temp _new_loadout.slots append from storage mgs:temp _sec_mag

# Increment inv_slot counter
scoreboard players add #inv_slot mgs.data 1

# Remove processed and recurse
data remove storage mgs:temp _build.secondary_data.mag_slots[0]
execute if data storage mgs:temp _build.secondary_data.mag_slots[0] run function mgs:v5.0.0/multiplayer/editor/append_sec_mags

