
#> mgs:v5.0.0/zombies/pap/on_right_click
#
# @within	???
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

# Deduct points and apply runtime overrides from pap_stats
scoreboard players operation @s mgs.zb.points -= #pap_price mgs.data
function mgs:v5.0.0/zombies/pap/apply_runtime_overrides

# Keep level tracking in the weapon data itself
execute store result storage mgs:temp _pap_extract.stats.pap_level int 1 run scoreboard players get #pap_next mgs.data

# Optional runtime PAP name override
execute if data storage mgs:temp _pap_extract.stats.pap_stats.pap_name run function mgs:v5.0.0/zombies/pap/resolve_runtime_name

# Lore visual marker for current PAP level
execute if data storage mgs:temp _pap_extract.lore[0] run function mgs:v5.0.0/zombies/pap/append_level_to_lore

# Preserve common refill behavior: if capacity is overridden and no explicit remaining_bullets override,
# refill to the new capacity for this upgrade.
execute if data storage mgs:temp _pap_extract.stats.pap_stats.capacity unless data storage mgs:temp _pap_extract.stats.pap_stats.remaining_bullets run data modify storage mgs:temp _pap_extract.stats.remaining_bullets set from storage mgs:temp _pap_extract.stats.capacity

# Apply to item and refresh ammo/lore
function mgs:v5.0.0/zombies/pap/apply_to_slot with storage mgs:temp _pap
function mgs:v5.0.0/ammo/compute_reserve

# Message and feedback
execute store result storage mgs:temp _pap_buy.id int 1 run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.pap.id
function mgs:v5.0.0/zombies/pap/lookup_machine with storage mgs:temp _pap_buy
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.upgraded_via","color":"green"},{"storage":"mgs:temp","nbt":"_pap_machine.name","color":"gold","interpret":true},[{"text":" ","color":"green"}, {"translate":"mgs.to_level"}],{"score":{"name":"#pap_next","objective":"mgs.data"},"color":"yellow"},{"text":".","color":"green"}]
function mgs:v5.0.0/zombies/feedback/sound_success

