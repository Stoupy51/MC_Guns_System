
#> mgs:v5.1.0/zombies/pap/upgrade_core
#
# @executed	as @p[tag=mgs.pu_collecting]
#
# @within	mgs:v5.1.0/zombies/pap/on_free_pap
#

# Must be hotbar 1, 2 or 3.
execute store result score #pap_sel mgs.data run data get entity @s SelectedItemSlot
execute unless score #pap_sel mgs.data matches 1..3 run return run function mgs:v5.1.0/zombies/deny/message {msg:'{"translate":"mgs.hold_weapon_slot_1_2_or_3_to_use_pack_a_punch","color":"red"}'}

scoreboard players set #pap_is_gun mgs.data 0
execute if score #pap_sel mgs.data matches 1 if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true}}] run scoreboard players set #pap_is_gun mgs.data 1
execute if score #pap_sel mgs.data matches 2 if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true}}] run scoreboard players set #pap_is_gun mgs.data 1
execute if score #pap_sel mgs.data matches 3 if items entity @s hotbar.3 *[custom_data~{mgs:{gun:true}}] run scoreboard players set #pap_is_gun mgs.data 1
execute unless score #pap_is_gun mgs.data matches 1 run return run function mgs:v5.1.0/zombies/deny/message {msg:'{"translate":"mgs.selected_slot_does_not_contain_a_weapon","color":"red"}'}

data modify storage mgs:temp _pap.slot set value "hotbar.1"
execute if score #pap_sel mgs.data matches 2 run data modify storage mgs:temp _pap.slot set value "hotbar.2"
execute if score #pap_sel mgs.data matches 3 run data modify storage mgs:temp _pap.slot set value "hotbar.3"

function mgs:v5.1.0/zombies/pap/extract_selected with storage mgs:temp _pap

execute unless data storage mgs:temp _pap_extract.stats.pap_stats run return run function mgs:v5.1.0/zombies/deny/message {msg:'{"translate":"mgs.this_weapon_cannot_be_pack_a_punched","color":"red"}'}

scoreboard players set #pap_level mgs.data 0
execute if data storage mgs:temp _pap_extract.stats.pap_level store result score #pap_level mgs.data run data get storage mgs:temp _pap_extract.stats.pap_level
scoreboard players operation #pap_next mgs.data = #pap_level mgs.data
scoreboard players add #pap_next mgs.data 1
scoreboard players operation #pap_next_idx mgs.data = #pap_next mgs.data
scoreboard players remove #pap_next_idx mgs.data 1

function mgs:v5.1.0/zombies/pap/compute_max_level

# Already at max: a free scope and camo re-roll.
execute if score #pap_next mgs.data > #pap_max mgs.data run return run function mgs:v5.1.0/zombies/pap/free_scope_reroll with storage mgs:temp _pap

# Kept for the lore annotation.
data modify storage mgs:temp _pap_old_stats set from storage mgs:temp _pap_extract.stats

function mgs:v5.1.0/zombies/pap/apply_runtime_overrides

# Applied directly, no animation.
function mgs:v5.1.0/zombies/pap/randomize_scope with storage mgs:temp _pap_extract.stats
function mgs:v5.1.0/zombies/pap/randomize_camo with storage mgs:temp _pap_extract.stats

execute store result storage mgs:temp _pap_extract.stats.pap_level int 1 run scoreboard players get #pap_next mgs.data

# PAP name when there is one, else the current one.
execute if data storage mgs:temp _pap_extract.stats.pap_stats.pap_name run function mgs:v5.1.0/zombies/pap/resolve_runtime_name
execute if data storage mgs:temp _pap_extract.new_name run data modify storage mgs:temp _pap_name_data.name set from storage mgs:temp _pap_extract.new_name
execute unless data storage mgs:temp _pap_extract.new_name run data modify storage mgs:temp _pap_name_data.name set from storage mgs:temp _pap_extract.current_name
execute store result storage mgs:temp _pap_name_data.level int 1 run scoreboard players get #pap_next mgs.data
execute store result storage mgs:temp _pap_name_data.max int 1 run scoreboard players get #pap_max mgs.data

# The annotation would break the "/" pattern modify_lore searches for.
execute if data storage mgs:temp _pap_extract.lore[1] run data modify storage mgs:temp _pap_lore1_original set from storage mgs:temp _pap_extract.lore[1]

execute if data storage mgs:temp _pap_extract.lore[0] run function mgs:v5.1.0/zombies/pap/annotate_lore

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"✦ ",{"translate":"mgs.pack_a_punch_3","color":"aqua","bold":true},[{"text":"  ","color":"gray"}, {"translate":"mgs.level_2"}],{"score":{"name":"#pap_next","objective":"mgs.data"},"color":"aqua"},{"text":"/","color":"dark_gray"},{"score":{"name":"#pap_max","objective":"mgs.data"},"color":"aqua"}]
playsound minecraft:entity.experience_orb.pickup ambient @s ~ ~ ~ 0.8 1.25

execute if data storage mgs:temp _pap_lore1_original run data modify storage mgs:temp _pap_extract.lore[1] set from storage mgs:temp _pap_lore1_original

data modify storage mgs:temp _pap_extract.stats.remaining_bullets set from storage mgs:temp _pap_extract.stats.capacity

function mgs:v5.1.0/zombies/pap/apply_to_slot with storage mgs:temp _pap

# 8x the weapon capacity.
function mgs:v5.1.0/zombies/pap/pap_upgrade_magazines with storage mgs:temp _pap_extract.stats

function mgs:v5.1.0/ammo/compute_reserve

