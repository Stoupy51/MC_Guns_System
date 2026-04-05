
#> mgs:v5.0.0/zombies/pap/on_right_click
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/setup_iter {run:"function mgs:v5.0.0/zombies/pap/on_right_click",executor:"source"} [ as @n[tag=mgs.pap_new] ]
#

# Guard: game must be active
execute unless data storage mgs:zombies game{state:"active"} run return fail

# Guard: power requirement
execute store result score #pap_power mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.pap.power
execute if score #pap_power mgs.data matches 1 unless score #zb_power mgs.data matches 1 run return run function mgs:v5.0.0/zombies/pap/deny_requires_power

# Guard: player has enough points
execute store result score #pap_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.pap.price
execute unless score @s mgs.zb.points >= #pap_price mgs.data run return run function mgs:v5.0.0/zombies/pap/deny_not_enough_points

# Determine selected zombies weapon slot (must be hotbar.1/2/3)
execute store result score #pap_sel mgs.data run data get entity @s SelectedItemSlot
execute unless score #pap_sel mgs.data matches 1..3 run return run function mgs:v5.0.0/zombies/pap/deny_hold_weapon_slot

data modify storage mgs:temp _pap.slot set value "hotbar.1"
execute if score #pap_sel mgs.data matches 2 run data modify storage mgs:temp _pap.slot set value "hotbar.2"
execute if score #pap_sel mgs.data matches 3 run data modify storage mgs:temp _pap.slot set value "hotbar.3"

# Guard: selected slot must contain a gun item
scoreboard players set #pap_is_gun mgs.data 0
execute if score #pap_sel mgs.data matches 1 if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true}}] run scoreboard players set #pap_is_gun mgs.data 1
execute if score #pap_sel mgs.data matches 2 if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true}}] run scoreboard players set #pap_is_gun mgs.data 1
execute if score #pap_sel mgs.data matches 3 if items entity @s hotbar.3 *[custom_data~{mgs:{gun:true}}] run scoreboard players set #pap_is_gun mgs.data 1
execute unless score #pap_is_gun mgs.data matches 1 run return run function mgs:v5.0.0/zombies/pap/deny_not_gun

# Extract selected item data
function mgs:v5.0.0/zombies/pap/extract_selected with storage mgs:temp _pap

# Guard: selected weapon must provide PAP data in its own stats
execute unless data storage mgs:temp _pap_extract.stats.pap_stats run return run function mgs:v5.0.0/zombies/pap/deny_not_supported

# Compute current and next PAP levels
scoreboard players set #pap_level mgs.data 0
execute if data storage mgs:temp _pap_extract.stats.pap_level store result score #pap_level mgs.data run data get storage mgs:temp _pap_extract.stats.pap_level
scoreboard players operation #pap_next mgs.data = #pap_level mgs.data
scoreboard players add #pap_next mgs.data 1
scoreboard players operation #pap_next_idx mgs.data = #pap_next mgs.data
scoreboard players remove #pap_next_idx mgs.data 1

# Guard: next level must be <= runtime max derived from pap_stats lists
function mgs:v5.0.0/zombies/pap/compute_max_level
execute if score #pap_next mgs.data > #pap_max mgs.data run return run function mgs:v5.0.0/zombies/pap/deny_max_level

# Backup visible stats for lore annotation before overrides
data modify storage mgs:temp _pap_old_stats set from storage mgs:temp _pap_extract.stats

# Deduct points and apply runtime overrides from pap_stats
scoreboard players operation @s mgs.zb.points -= #pap_price mgs.data
function mgs:v5.0.0/zombies/pap/apply_runtime_overrides

# Keep level tracking in the weapon data itself
execute store result storage mgs:temp _pap_extract.stats.pap_level int 1 run scoreboard players get #pap_next mgs.data

# Resolve pre-built PAP display name with level suffix
execute if data storage mgs:temp _pap_extract.stats.pap_stats.pap_name run function mgs:v5.0.0/zombies/pap/resolve_runtime_name

# Prepare name data: use PAP name if available, otherwise keep original
execute if data storage mgs:temp _pap_extract.new_name run data modify storage mgs:temp _pap_name_data.name set from storage mgs:temp _pap_extract.new_name
execute unless data storage mgs:temp _pap_extract.new_name run data modify storage mgs:temp _pap_name_data.name set from storage mgs:temp _pap_extract.current_name
execute store result storage mgs:temp _pap_name_data.level int 1 run scoreboard players get #pap_next mgs.data
execute store result storage mgs:temp _pap_name_data.max int 1 run scoreboard players get #pap_max mgs.data

# Annotate lore lines with runtime-computed PAP deltas
execute if data storage mgs:temp _pap_extract.lore[0] run function mgs:v5.0.0/zombies/pap/annotate_lore

# Always refill gun ammo to max capacity on PAP
data modify storage mgs:temp _pap_extract.stats.remaining_bullets set from storage mgs:temp _pap_extract.stats.capacity

# Apply to item, refill matching magazines, and refresh ammo display
function mgs:v5.0.0/zombies/pap/apply_to_slot with storage mgs:temp _pap
function mgs:v5.0.0/zombies/pap/refill_matching_magazines with storage mgs:temp _pap_extract.stats
function mgs:v5.0.0/ammo/compute_reserve

# Message and feedback
execute store result storage mgs:temp _pap_buy.id int 1 run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.pap.id
function mgs:v5.0.0/zombies/pap/lookup_machine with storage mgs:temp _pap_buy
function mgs:v5.0.0/zombies/pap/pap_chat_message
function mgs:v5.0.0/zombies/feedback/sound_success

