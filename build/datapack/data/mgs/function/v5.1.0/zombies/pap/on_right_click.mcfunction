
#> mgs:v5.1.0/zombies/pap/on_right_click
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.1.0/zombies/pap/setup_iter {run:"function mgs:v5.1.0/zombies/pap/on_right_click",executor:"source"} [ as @n[tag=mgs.pap_new] ]
#

execute unless data storage mgs:zombies game{state:"active"} run return fail

# Retreat phase (1..205): the weapon can be collected.
execute if score @n[tag=bs.interaction.target] mgs.pap_anim matches 1..205 run return run function mgs:v5.1.0/zombies/pap/anim/collect
# Sliding in, inside or sliding out: not collectible yet.
execute if score @n[tag=bs.interaction.target] mgs.pap_anim matches 206.. run return run function mgs:v5.1.0/zombies/deny/message {msg:'{"translate":"mgs.already_processing_a_weapon","color":"yellow"}'}

execute store result score #pap_power mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.pap.power
execute if score #pap_power mgs.data matches 1 unless score #zb_power mgs.data matches 1 run return run function mgs:v5.1.0/zombies/deny/message {msg:'{"translate":"mgs.this_pack_a_punch_machine_requires_power","color":"red"}'}

execute store result score #pap_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.pap.price
execute if score #zb_bonfire_sale_timer mgs.data matches 1.. run scoreboard players set #pap_price mgs.data 1000
execute unless score @s mgs.zb.points >= #pap_price mgs.data run return run function mgs:v5.1.0/zombies/deny/not_enough_points {score:"#pap_price",obj:"mgs.data"}

# Must be hotbar.1, 2 or 3.
execute store result score #pap_sel mgs.data run data get entity @s SelectedItemSlot
execute unless score #pap_sel mgs.data matches 1..3 run return run function mgs:v5.1.0/zombies/deny/message {msg:'{"translate":"mgs.hold_weapon_slot_1_2_or_3_to_use_pack_a_punch","color":"red"}'}

data modify storage mgs:temp _pap.slot set value "hotbar.1"
execute if score #pap_sel mgs.data matches 2 run data modify storage mgs:temp _pap.slot set value "hotbar.2"
execute if score #pap_sel mgs.data matches 3 run data modify storage mgs:temp _pap.slot set value "hotbar.3"

scoreboard players set #pap_is_gun mgs.data 0
execute if score #pap_sel mgs.data matches 1 if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true}}] run scoreboard players set #pap_is_gun mgs.data 1
execute if score #pap_sel mgs.data matches 2 if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true}}] run scoreboard players set #pap_is_gun mgs.data 1
execute if score #pap_sel mgs.data matches 3 if items entity @s hotbar.3 *[custom_data~{mgs:{gun:true}}] run scoreboard players set #pap_is_gun mgs.data 1
execute unless score #pap_is_gun mgs.data matches 1 run return run function mgs:v5.1.0/zombies/deny/message {msg:'{"translate":"mgs.selected_slot_does_not_contain_a_weapon","color":"red"}'}

function mgs:v5.1.0/zombies/pap/extract_selected with storage mgs:temp _pap

# The weapon's own stats must carry PAP data.
execute unless data storage mgs:temp _pap_extract.stats.pap_stats run return run function mgs:v5.1.0/zombies/deny/message {msg:'{"translate":"mgs.this_weapon_cannot_be_pack_a_punched","color":"red"}'}

scoreboard players set #pap_level mgs.data 0
execute if data storage mgs:temp _pap_extract.stats.pap_level store result score #pap_level mgs.data run data get storage mgs:temp _pap_extract.stats.pap_level
scoreboard players operation #pap_next mgs.data = #pap_level mgs.data
scoreboard players add #pap_next mgs.data 1
scoreboard players operation #pap_next_idx mgs.data = #pap_next mgs.data
scoreboard players remove #pap_next_idx mgs.data 1

# The max level comes from the longest pap_stats list.
function mgs:v5.1.0/zombies/pap/compute_max_level
execute if score #pap_next mgs.data > #pap_max mgs.data run return run function mgs:v5.1.0/zombies/pap/repap_scope_only with storage mgs:temp _pap

# Kept for the lore annotation.
data modify storage mgs:temp _pap_old_stats set from storage mgs:temp _pap_extract.stats

scoreboard players operation @s mgs.zb.points -= #pap_price mgs.data
function mgs:v5.1.0/zombies/pap/apply_runtime_overrides

# Silent award: the machine animation is the confirmation.
function mgs:v5.1.0/progression/zb/award_pack_a_punch

data modify storage mgs:temp _pap_pre_cosm_weapon set from storage mgs:temp _pap_extract.weapon

function mgs:v5.1.0/zombies/pap/randomize_scope with storage mgs:temp _pap_extract.stats

# After the scope, so the camo appends to the scoped weapon id.
function mgs:v5.1.0/zombies/pap/randomize_camo with storage mgs:temp _pap_extract.stats

# Applied mid-animation, keyed by machine id.
data modify storage mgs:temp _pap_cosm_store set value {}
execute store result storage mgs:temp _pap_cosm_store.id int 1 run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.pap.id
data modify storage mgs:temp _pap_cosm_store.models set from storage mgs:temp _pap_extract.stats.models
data modify storage mgs:temp _pap_cosm_store.weapon set from storage mgs:temp _pap_extract.weapon
execute if data storage mgs:temp _pap_extract.stats.scope_level run data modify storage mgs:temp _pap_cosm_store.scope_level set from storage mgs:temp _pap_extract.stats.scope_level
function mgs:v5.1.0/zombies/pap/anim/store_cosmetics with storage mgs:temp _pap_cosm_store

# The item enters the machine with its current look.
data modify storage mgs:temp _pap_extract.stats.models set from storage mgs:temp _pap_old_stats.models
data modify storage mgs:temp _pap_extract.weapon set from storage mgs:temp _pap_pre_cosm_weapon
data remove storage mgs:temp _pap_extract.stats.scope_level
execute if data storage mgs:temp _pap_old_stats.scope_level run data modify storage mgs:temp _pap_extract.stats.scope_level set from storage mgs:temp _pap_old_stats.scope_level

execute store result storage mgs:temp _pap_extract.stats.pap_level int 1 run scoreboard players get #pap_next mgs.data

execute if data storage mgs:temp _pap_extract.stats.pap_stats.pap_name run function mgs:v5.1.0/zombies/pap/resolve_runtime_name

# PAP name when there is one, else the original.
execute if data storage mgs:temp _pap_extract.new_name run data modify storage mgs:temp _pap_name_data.name set from storage mgs:temp _pap_extract.new_name
execute unless data storage mgs:temp _pap_extract.new_name run data modify storage mgs:temp _pap_name_data.name set from storage mgs:temp _pap_extract.current_name
execute store result storage mgs:temp _pap_name_data.level int 1 run scoreboard players get #pap_next mgs.data
execute store result storage mgs:temp _pap_name_data.max int 1 run scoreboard players get #pap_max mgs.data

# The annotation would break the "/" pattern modify_lore searches for, so the ammo line is backed up.
execute if data storage mgs:temp _pap_extract.lore[1] run data modify storage mgs:temp _pap_lore1_original set from storage mgs:temp _pap_extract.lore[1]

execute if data storage mgs:temp _pap_extract.lore[0] run function mgs:v5.1.0/zombies/pap/annotate_lore

# Detailed stats in chat, before the ammo line is restored.
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.pack_a_punching_your_weapon","color":"aqua"}]
execute store result storage mgs:temp _pap_hover.id int 1 run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.pap.id
function mgs:v5.1.0/zombies/pap/lookup_machine with storage mgs:temp _pap_hover
function mgs:v5.1.0/zombies/pap/pap_chat_message

execute if data storage mgs:temp _pap_lore1_original run data modify storage mgs:temp _pap_extract.lore[1] set from storage mgs:temp _pap_lore1_original

data modify storage mgs:temp _pap_extract.stats.remaining_bullets set from storage mgs:temp _pap_extract.stats.capacity

# Also upgrades and refills the matching magazines (8x capacity).
function mgs:v5.1.0/zombies/pap/apply_to_slot with storage mgs:temp _pap
function mgs:v5.1.0/zombies/pap/pap_upgrade_magazines with storage mgs:temp _pap_extract.stats
function mgs:v5.1.0/ammo/compute_reserve

tag @s add mgs.pap_owner
scoreboard players operation @s mgs.zb.pap_s = #pap_sel mgs.data
execute store result score @s mgs.zb.pap_mid run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.pap.id
execute as @n[tag=bs.interaction.target] at @s run function mgs:v5.1.0/zombies/pap/anim/start with storage mgs:temp _pap
tag @s remove mgs.pap_owner

