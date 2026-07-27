""" Buying an upgrade: the guards, the point cost and the re-roll at max level. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.stats.keys import PAP_STATS, REMAINING_BULLETS
from ....core.feedback import ZombiesFeedback
from ....helpers import MGS_TAG
from ...common import ZombiesCommon
from .shared import REPAP_SCOPE_PRICE


# Functions
def write_pap_purchase() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	gun_cd: str = ZombiesCommon.gun_cd(ns)

	deny_requires_power: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"This Pack-a-Punch machine requires power.","color":"red"}')
	deny_hold_weapon_slot: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"Hold weapon slot 1, 2, or 3 to use Pack-a-Punch.","color":"red"}')
	deny_not_gun: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"Selected slot does not contain a weapon.","color":"red"}')
	deny_not_supported: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"This weapon cannot be Pack-a-Punched.","color":"red"}')
	deny_not_enough_points: str = ZombiesCommon.deny_not_enough_points_cmd(ns, version, "#pap_price")
	deny_processing: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"Already processing a weapon...","color":"yellow"}')

	## Re-PAP at max level: scope/camo only randomization for a reduced price
	write_versioned_function("zombies/pap/repap_scope_only", f"""
# Guard: enough points for scope/camo re-roll
execute unless score @s {ns}.zb.points matches {REPAP_SCOPE_PRICE}.. run return run function {ns}:v{version}/zombies/pap/deny_not_enough_points_scope

# Deduct points
scoreboard players remove @s {ns}.zb.points {REPAP_SCOPE_PRICE}

# Save current weapon ID and models before scope randomization (for restore)
data modify storage {ns}:temp _pap_old_weapon set from storage {ns}:temp _pap_extract.weapon
data modify storage {ns}:temp _pap_pre_cosm_models set from storage {ns}:temp _pap_extract.stats.models
data remove storage {ns}:temp _pap_pre_cosm_scope_level
execute if data storage {ns}:temp _pap_extract.stats.scope_level run data modify storage {ns}:temp _pap_pre_cosm_scope_level set from storage {ns}:temp _pap_extract.stats.scope_level

# Randomize weapon scope (retry until different from current)
function {ns}:v{version}/zombies/pap/randomize_scope_different with storage {ns}:temp _pap_extract.stats

# Randomize camo (uses new scope weapon_id, same base_weapon)
function {ns}:v{version}/zombies/pap/randomize_camo with storage {ns}:temp _pap_extract.stats

# Store pending cosmetics (scope + camo) for mid-animation application, keyed by machine ID
data modify storage {ns}:temp _pap_cosm_store set value {{}}
execute store result storage {ns}:temp _pap_cosm_store.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.pap.id
data modify storage {ns}:temp _pap_cosm_store.models set from storage {ns}:temp _pap_extract.stats.models
data modify storage {ns}:temp _pap_cosm_store.weapon set from storage {ns}:temp _pap_extract.weapon
execute if data storage {ns}:temp _pap_extract.stats.scope_level run data modify storage {ns}:temp _pap_cosm_store.scope_level set from storage {ns}:temp _pap_extract.stats.scope_level
function {ns}:v{version}/zombies/pap/anim/store_cosmetics with storage {ns}:temp _pap_cosm_store

# Restore original appearance so the item enters the machine with its current look
data modify storage {ns}:temp _pap_extract.stats.models set from storage {ns}:temp _pap_pre_cosm_models
data modify storage {ns}:temp _pap_extract.weapon set from storage {ns}:temp _pap_old_weapon
data remove storage {ns}:temp _pap_extract.stats.scope_level
execute if data storage {ns}:temp _pap_pre_cosm_scope_level run data modify storage {ns}:temp _pap_extract.stats.scope_level set from storage {ns}:temp _pap_pre_cosm_scope_level

# Apply stats to item (with restored original cosmetics)
$item modify entity @s $(slot) {ns}:v{version}/zb_pap_apply_stats

# Brief feedback
tellraw @s [{MGS_TAG},{{"text":"Scope re-rolled! (-{REPAP_SCOPE_PRICE} points)","color":"aqua"}}]

# Start PAP animation
tag @s add {ns}.pap_owner
scoreboard players operation @s {ns}.zb.pap_s = #pap_sel {ns}.data
execute store result score @s {ns}.zb.pap_mid run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.pap.id
execute as @n[tag=bs.interaction.target] at @s run function {ns}:v{version}/zombies/pap/anim/start with storage {ns}:temp _pap
tag @s remove {ns}.pap_owner
""")

	write_versioned_function("zombies/pap/deny_not_enough_points_scope", f"""
tellraw @s [{MGS_TAG},{{"text":"You don't have enough points ({REPAP_SCOPE_PRICE} needed).","color":"red"}}]
{ZombiesFeedback.zb_sound('deny')}
""")

	write_versioned_function("zombies/pap/on_right_click", f"""
# Guard: game must be active
{ZombiesCommon.game_active_guard_cmd(ns)}

# If weapon is in retreat/collectible phase (1..205): allow collection
execute if score @n[tag=bs.interaction.target] {ns}.pap_anim matches 1..205 run return run function {ns}:v{version}/zombies/pap/anim/collect
# If machine is going-in, inside, or coming-out (not yet collectible), deny
execute if score @n[tag=bs.interaction.target] {ns}.pap_anim matches 206.. run return run {deny_processing}

# Guard: power requirement
execute store result score #pap_power {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.pap.power
execute if score #pap_power {ns}.data matches 1 unless score #zb_power {ns}.data matches 1 run return run {deny_requires_power}

# Guard: player has enough points
execute store result score #pap_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.pap.price
# Bonfire Sale: Pack-a-Punch costs 1000 while active
execute if score #zb_bonfire_sale_timer {ns}.data matches 1.. run scoreboard players set #pap_price {ns}.data 1000
execute unless score @s {ns}.zb.points >= #pap_price {ns}.data run return run {deny_not_enough_points}

# Determine selected zombies weapon slot (must be hotbar.1/2/3)
execute store result score #pap_sel {ns}.data run data get entity @s SelectedItemSlot
execute unless score #pap_sel {ns}.data matches 1..3 run return run {deny_hold_weapon_slot}

data modify storage {ns}:temp _pap.slot set value "hotbar.1"
execute if score #pap_sel {ns}.data matches 2 run data modify storage {ns}:temp _pap.slot set value "hotbar.2"
execute if score #pap_sel {ns}.data matches 3 run data modify storage {ns}:temp _pap.slot set value "hotbar.3"

# Guard: selected slot must contain a gun item
scoreboard players set #pap_is_gun {ns}.data 0
execute if score #pap_sel {ns}.data matches 1 if items entity @s hotbar.1 *[custom_data~{gun_cd}] run scoreboard players set #pap_is_gun {ns}.data 1
execute if score #pap_sel {ns}.data matches 2 if items entity @s hotbar.2 *[custom_data~{gun_cd}] run scoreboard players set #pap_is_gun {ns}.data 1
execute if score #pap_sel {ns}.data matches 3 if items entity @s hotbar.3 *[custom_data~{gun_cd}] run scoreboard players set #pap_is_gun {ns}.data 1
execute unless score #pap_is_gun {ns}.data matches 1 run return run {deny_not_gun}

# Extract selected item data
function {ns}:v{version}/zombies/pap/extract_selected with storage {ns}:temp _pap

# Guard: selected weapon must provide PAP data in its own stats
execute unless data storage {ns}:temp _pap_extract.stats.{PAP_STATS} run return run {deny_not_supported}

# Compute current and next PAP levels
scoreboard players set #pap_level {ns}.data 0
execute if data storage {ns}:temp _pap_extract.stats.pap_level store result score #pap_level {ns}.data run data get storage {ns}:temp _pap_extract.stats.pap_level
scoreboard players operation #pap_next {ns}.data = #pap_level {ns}.data
scoreboard players add #pap_next {ns}.data 1
scoreboard players operation #pap_next_idx {ns}.data = #pap_next {ns}.data
scoreboard players remove #pap_next_idx {ns}.data 1

# Guard: next level must be <= runtime max derived from pap_stats lists
function {ns}:v{version}/zombies/pap/compute_max_level
execute if score #pap_next {ns}.data > #pap_max {ns}.data run return run function {ns}:v{version}/zombies/pap/repap_scope_only with storage {ns}:temp _pap

# Backup visible stats for lore annotation before overrides
data modify storage {ns}:temp _pap_old_stats set from storage {ns}:temp _pap_extract.stats

# Deduct points and apply runtime overrides from pap_stats
scoreboard players operation @s {ns}.zb.points -= #pap_price {ns}.data
function {ns}:v{version}/zombies/pap/apply_runtime_overrides

# Save original weapon ID before scope randomization (for later restore)
data modify storage {ns}:temp _pap_pre_cosm_weapon set from storage {ns}:temp _pap_extract.weapon

# Randomize weapon scope
function {ns}:v{version}/zombies/pap/randomize_scope with storage {ns}:temp _pap_extract.stats

# Randomize weapon camo (applied after scope, so camo appends to the scoped weapon id)
function {ns}:v{version}/zombies/pap/randomize_camo with storage {ns}:temp _pap_extract.stats

# Store pending cosmetics (scope + camo) for mid-animation application, keyed by machine ID
data modify storage {ns}:temp _pap_cosm_store set value {{}}
execute store result storage {ns}:temp _pap_cosm_store.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.pap.id
data modify storage {ns}:temp _pap_cosm_store.models set from storage {ns}:temp _pap_extract.stats.models
data modify storage {ns}:temp _pap_cosm_store.weapon set from storage {ns}:temp _pap_extract.weapon
execute if data storage {ns}:temp _pap_extract.stats.scope_level run data modify storage {ns}:temp _pap_cosm_store.scope_level set from storage {ns}:temp _pap_extract.stats.scope_level
function {ns}:v{version}/zombies/pap/anim/store_cosmetics with storage {ns}:temp _pap_cosm_store

# Restore original appearance so the item enters the machine with its current look
data modify storage {ns}:temp _pap_extract.stats.models set from storage {ns}:temp _pap_old_stats.models
data modify storage {ns}:temp _pap_extract.weapon set from storage {ns}:temp _pap_pre_cosm_weapon
data remove storage {ns}:temp _pap_extract.stats.scope_level
execute if data storage {ns}:temp _pap_old_stats.scope_level run data modify storage {ns}:temp _pap_extract.stats.scope_level set from storage {ns}:temp _pap_old_stats.scope_level

# Keep level tracking in the weapon data itself
execute store result storage {ns}:temp _pap_extract.stats.pap_level int 1 run scoreboard players get #pap_next {ns}.data

# Resolve pre-built PAP display name with level suffix
execute if data storage {ns}:temp _pap_extract.stats.{PAP_STATS}.pap_name run function {ns}:v{version}/zombies/pap/resolve_runtime_name

# Prepare name data: use PAP name if available, otherwise keep original
execute if data storage {ns}:temp _pap_extract.new_name run data modify storage {ns}:temp _pap_name_data.name set from storage {ns}:temp _pap_extract.new_name
execute unless data storage {ns}:temp _pap_extract.new_name run data modify storage {ns}:temp _pap_name_data.name set from storage {ns}:temp _pap_extract.current_name
execute store result storage {ns}:temp _pap_name_data.level int 1 run scoreboard players get #pap_next {ns}.data
execute store result storage {ns}:temp _pap_name_data.max int 1 run scoreboard players get #pap_max {ns}.data

# Backup ammo lore line before annotation (annotation would break modify_lore search pattern)
execute if data storage {ns}:temp _pap_extract.lore[1] run data modify storage {ns}:temp _pap_lore1_original set from storage {ns}:temp _pap_extract.lore[1]

# Annotate lore lines with runtime-computed PAP deltas
execute if data storage {ns}:temp _pap_extract.lore[0] run function {ns}:v{version}/zombies/pap/annotate_lore

# Show detailed PAP stats in chat (before restoring unannotated ammo line)
tellraw @s [{MGS_TAG},{{"text":"Pack-a-Punching your weapon...","color":"aqua"}}]
execute store result storage {ns}:temp _pap_hover.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.pap.id
function {ns}:v{version}/zombies/pap/lookup_machine with storage {ns}:temp _pap_hover
function {ns}:v{version}/zombies/pap/pap_chat_message

# Restore unannotated ammo line for item (preserves "/" pattern for modify_lore)
execute if data storage {ns}:temp _pap_lore1_original run data modify storage {ns}:temp _pap_extract.lore[1] set from storage {ns}:temp _pap_lore1_original

# Always refill gun ammo to max capacity on PAP
data modify storage {ns}:temp _pap_extract.stats.{REMAINING_BULLETS} set from storage {ns}:temp _pap_extract.stats.capacity

# Apply to item, upgrade+refill matching magazines (8x capacity), and refresh ammo display
function {ns}:v{version}/zombies/pap/apply_to_slot with storage {ns}:temp _pap
function {ns}:v{version}/zombies/pap/pap_upgrade_magazines with storage {ns}:temp _pap_extract.stats
function {ns}:v{version}/ammo/compute_reserve

# Take weapon from player and start PAP animation
tag @s add {ns}.pap_owner
scoreboard players operation @s {ns}.zb.pap_s = #pap_sel {ns}.data
execute store result score @s {ns}.zb.pap_mid run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.pap.id
execute as @n[tag=bs.interaction.target] at @s run function {ns}:v{version}/zombies/pap/anim/start with storage {ns}:temp _pap
tag @s remove {ns}.pap_owner
""")

