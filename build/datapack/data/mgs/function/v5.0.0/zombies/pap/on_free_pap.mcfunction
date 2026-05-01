
#> mgs:v5.0.0/zombies/pap/on_free_pap
#
# @executed	as @p[tag=mgs.pu_collecting]
#
# @within	mgs:v5.0.0/zombies/powerups/activate/free_pap [ as @p[tag=mgs.pu_collecting] ]
#

# Guard: game must be active
execute unless data storage mgs:zombies game{state:"active"} run return fail

# Determine selected weapon slot (must be hotbar 1, 2, or 3)
execute store result score #pap_sel mgs.data run data get entity @s SelectedItemSlot
execute unless score #pap_sel mgs.data matches 1..3 run return run function mgs:v5.0.0/zombies/pap/deny_hold_weapon_slot

# Guard: selected slot must contain a gun
scoreboard players set #pap_is_gun mgs.data 0
execute if score #pap_sel mgs.data matches 1 if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true}}] run scoreboard players set #pap_is_gun mgs.data 1
execute if score #pap_sel mgs.data matches 2 if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true}}] run scoreboard players set #pap_is_gun mgs.data 1
execute if score #pap_sel mgs.data matches 3 if items entity @s hotbar.3 *[custom_data~{mgs:{gun:true}}] run scoreboard players set #pap_is_gun mgs.data 1
execute unless score #pap_is_gun mgs.data matches 1 run return run function mgs:v5.0.0/zombies/pap/deny_not_gun

# Resolve slot string
data modify storage mgs:temp _pap.slot set value "hotbar.1"
execute if score #pap_sel mgs.data matches 2 run data modify storage mgs:temp _pap.slot set value "hotbar.2"
execute if score #pap_sel mgs.data matches 3 run data modify storage mgs:temp _pap.slot set value "hotbar.3"

# Extract gun data from the selected slot
function mgs:v5.0.0/zombies/pap/extract_selected with storage mgs:temp _pap

# Guard: weapon must support PAP
execute unless data storage mgs:temp _pap_extract.stats.pap_stats run return run function mgs:v5.0.0/zombies/pap/deny_not_supported

# Compute current and next PAP levels
scoreboard players set #pap_level mgs.data 0
execute if data storage mgs:temp _pap_extract.stats.pap_level store result score #pap_level mgs.data run data get storage mgs:temp _pap_extract.stats.pap_level
scoreboard players operation #pap_next mgs.data = #pap_level mgs.data
scoreboard players add #pap_next mgs.data 1
scoreboard players operation #pap_next_idx mgs.data = #pap_next mgs.data
scoreboard players remove #pap_next_idx mgs.data 1

# Compute runtime max from pap_stats list lengths
function mgs:v5.0.0/zombies/pap/compute_max_level

# If already at max level: free scope/camo reroll only
execute if score #pap_next mgs.data > #pap_max mgs.data run return run function mgs:v5.0.0/zombies/pap/free_scope_reroll with storage mgs:temp _pap

# Backup visible stats for lore annotation before overrides
data modify storage mgs:temp _pap_old_stats set from storage mgs:temp _pap_extract.stats

# Apply stat overrides from pap_stats (no point cost)
function mgs:v5.0.0/zombies/pap/apply_runtime_overrides

# Randomize scope and camo (applied directly — no animation)
function mgs:v5.0.0/zombies/pap/randomize_scope with storage mgs:temp _pap_extract.stats
function mgs:v5.0.0/zombies/pap/randomize_camo with storage mgs:temp _pap_extract.stats

# Update PAP level in item data
execute store result storage mgs:temp _pap_extract.stats.pap_level int 1 run scoreboard players get #pap_next mgs.data

# Resolve display name (PAP-specific name or keep current)
execute if data storage mgs:temp _pap_extract.stats.pap_stats.pap_name run function mgs:v5.0.0/zombies/pap/resolve_runtime_name
execute if data storage mgs:temp _pap_extract.new_name run data modify storage mgs:temp _pap_name_data.name set from storage mgs:temp _pap_extract.new_name
execute unless data storage mgs:temp _pap_extract.new_name run data modify storage mgs:temp _pap_name_data.name set from storage mgs:temp _pap_extract.current_name
execute store result storage mgs:temp _pap_name_data.level int 1 run scoreboard players get #pap_next mgs.data
execute store result storage mgs:temp _pap_name_data.max int 1 run scoreboard players get #pap_max mgs.data

# Backup ammo lore line before annotation
execute if data storage mgs:temp _pap_extract.lore[1] run data modify storage mgs:temp _pap_lore1_original set from storage mgs:temp _pap_extract.lore[1]

# Annotate lore lines with stat deltas
execute if data storage mgs:temp _pap_extract.lore[0] run function mgs:v5.0.0/zombies/pap/annotate_lore

# Notify the player
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],[{"text":"✦ ","color":"aqua","bold":true}, {"translate":"mgs.free_pack_a_punch"}],[{"text":"  ","color":"gray"}, {"translate":"mgs.level"}],{"score":{"name":"#pap_next","objective":"mgs.data"},"color":"aqua"},{"text":"/","color":"dark_gray"},{"score":{"name":"#pap_max","objective":"mgs.data"},"color":"aqua"}]
function mgs:v5.0.0/zombies/feedback/sound_success

# Restore unannotated ammo lore (preserves "/" pattern for modify_lore)
execute if data storage mgs:temp _pap_lore1_original run data modify storage mgs:temp _pap_extract.lore[1] set from storage mgs:temp _pap_lore1_original

# Refill gun to full capacity
data modify storage mgs:temp _pap_extract.stats.remaining_bullets set from storage mgs:temp _pap_extract.stats.capacity

# Apply upgraded stats, name, and lore to the held weapon
function mgs:v5.0.0/zombies/pap/apply_to_slot with storage mgs:temp _pap

# Upgrade and refill matching magazines (8x weapon capacity)
function mgs:v5.0.0/zombies/pap/pap_upgrade_magazines with storage mgs:temp _pap_extract.stats

# Refresh ammo HUD
function mgs:v5.0.0/ammo/compute_reserve

