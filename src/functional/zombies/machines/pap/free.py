""" The unguarded upgrade core, the free power-up upgrade and the free re-roll at max level. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.keys import PAP_STATS, REMAINING_BULLETS
from ....core.feedback import ZombiesFeedback
from ....helpers import MGS_TAG
from ...common import ZombiesCommon


# Functions
def write_free_pap() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	gun_cd: str = ZombiesCommon.gun_cd(ns)

	deny_hold_weapon_slot: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"Hold weapon slot 1, 2, or 3 to use Pack-a-Punch.","color":"red"}')
	deny_not_gun: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"Selected slot does not contain a weapon.","color":"red"}')
	deny_not_supported: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"This weapon cannot be Pack-a-Punched.","color":"red"}')

	# PaP upgrade with no guard and no cost, for on_free_pap (guarded) and apply.
	write_versioned_function("zombies/pap/upgrade_core", f"""
# Must be hotbar 1, 2 or 3.
execute store result score #pap_sel {ns}.data run data get entity @s SelectedItemSlot
execute unless score #pap_sel {ns}.data matches 1..3 run return run {deny_hold_weapon_slot}

scoreboard players set #pap_is_gun {ns}.data 0
execute if score #pap_sel {ns}.data matches 1 if items entity @s hotbar.1 *[custom_data~{gun_cd}] run scoreboard players set #pap_is_gun {ns}.data 1
execute if score #pap_sel {ns}.data matches 2 if items entity @s hotbar.2 *[custom_data~{gun_cd}] run scoreboard players set #pap_is_gun {ns}.data 1
execute if score #pap_sel {ns}.data matches 3 if items entity @s hotbar.3 *[custom_data~{gun_cd}] run scoreboard players set #pap_is_gun {ns}.data 1
execute unless score #pap_is_gun {ns}.data matches 1 run return run {deny_not_gun}

data modify storage {ns}:temp _pap.slot set value "hotbar.1"
execute if score #pap_sel {ns}.data matches 2 run data modify storage {ns}:temp _pap.slot set value "hotbar.2"
execute if score #pap_sel {ns}.data matches 3 run data modify storage {ns}:temp _pap.slot set value "hotbar.3"

function {ns}:v{version}/zombies/pap/extract_selected with storage {ns}:temp _pap

execute unless data storage {ns}:temp _pap_extract.stats.{PAP_STATS} run return run {deny_not_supported}

scoreboard players set #pap_level {ns}.data 0
execute if data storage {ns}:temp _pap_extract.stats.pap_level store result score #pap_level {ns}.data run data get storage {ns}:temp _pap_extract.stats.pap_level
scoreboard players operation #pap_next {ns}.data = #pap_level {ns}.data
scoreboard players add #pap_next {ns}.data 1
scoreboard players operation #pap_next_idx {ns}.data = #pap_next {ns}.data
scoreboard players remove #pap_next_idx {ns}.data 1

function {ns}:v{version}/zombies/pap/compute_max_level

# Already at max: a free scope and camo re-roll.
execute if score #pap_next {ns}.data > #pap_max {ns}.data run return run function {ns}:v{version}/zombies/pap/free_scope_reroll with storage {ns}:temp _pap

# Kept for the lore annotation.
data modify storage {ns}:temp _pap_old_stats set from storage {ns}:temp _pap_extract.stats

function {ns}:v{version}/zombies/pap/apply_runtime_overrides

# Applied directly, no animation.
function {ns}:v{version}/zombies/pap/randomize_scope with storage {ns}:temp _pap_extract.stats
function {ns}:v{version}/zombies/pap/randomize_camo with storage {ns}:temp _pap_extract.stats

execute store result storage {ns}:temp _pap_extract.stats.pap_level int 1 run scoreboard players get #pap_next {ns}.data

# PAP name when there is one, else the current one.
execute if data storage {ns}:temp _pap_extract.stats.{PAP_STATS}.pap_name run function {ns}:v{version}/zombies/pap/resolve_runtime_name
execute if data storage {ns}:temp _pap_extract.new_name run data modify storage {ns}:temp _pap_name_data.name set from storage {ns}:temp _pap_extract.new_name
execute unless data storage {ns}:temp _pap_extract.new_name run data modify storage {ns}:temp _pap_name_data.name set from storage {ns}:temp _pap_extract.current_name
execute store result storage {ns}:temp _pap_name_data.level int 1 run scoreboard players get #pap_next {ns}.data
execute store result storage {ns}:temp _pap_name_data.max int 1 run scoreboard players get #pap_max {ns}.data

# The annotation would break the "/" pattern modify_lore searches for.
execute if data storage {ns}:temp _pap_extract.lore[1] run data modify storage {ns}:temp _pap_lore1_original set from storage {ns}:temp _pap_extract.lore[1]

execute if data storage {ns}:temp _pap_extract.lore[0] run function {ns}:v{version}/zombies/pap/annotate_lore

tellraw @s [{MGS_TAG},"✦ ",{{"text":"Pack-a-Punch!","color":"aqua","bold":true}},{{"text":"  Level ","color":"gray"}},{{"score":{{"name":"#pap_next","objective":"{ns}.data"}},"color":"aqua"}},{{"text":"/","color":"dark_gray"}},{{"score":{{"name":"#pap_max","objective":"{ns}.data"}},"color":"aqua"}}]
{ZombiesFeedback.zb_sound('success')}

execute if data storage {ns}:temp _pap_lore1_original run data modify storage {ns}:temp _pap_extract.lore[1] set from storage {ns}:temp _pap_lore1_original

data modify storage {ns}:temp _pap_extract.stats.{REMAINING_BULLETS} set from storage {ns}:temp _pap_extract.stats.capacity

function {ns}:v{version}/zombies/pap/apply_to_slot with storage {ns}:temp _pap

# 8x the weapon capacity.
function {ns}:v{version}/zombies/pap/pap_upgrade_magazines with storage {ns}:temp _pap_extract.stats

function {ns}:v{version}/ammo/compute_reserve
""")

	# Free PaP power-up.
	write_versioned_function("zombies/pap/on_free_pap", f"""
{ZombiesCommon.game_active_guard_cmd(ns)}
function {ns}:v{version}/zombies/pap/upgrade_core
""")

	# At max level: free scope and camo re-roll, no animation.
	write_versioned_function("zombies/pap/free_scope_reroll", f"""
function {ns}:v{version}/zombies/pap/randomize_scope_different with storage {ns}:temp _pap_extract.stats

function {ns}:v{version}/zombies/pap/randomize_camo with storage {ns}:temp _pap_extract.stats

data modify storage {ns}:temp _pap_name_data.name set from storage {ns}:temp _pap_extract.current_name
execute store result storage {ns}:temp _pap_name_data.level int 1 run scoreboard players get #pap_level {ns}.data
execute store result storage {ns}:temp _pap_name_data.max int 1 run scoreboard players get #pap_max {ns}.data

function {ns}:v{version}/zombies/pap/apply_to_slot with storage {ns}:temp _pap

tellraw @s [{MGS_TAG},"✦ ",{{"text":"Free scope/camo reroll! (already at max PAP level)","color":"aqua"}}]
{ZombiesFeedback.zb_sound('success')}
""")

