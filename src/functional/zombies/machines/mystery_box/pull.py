""" Starting a pull: the guards, the weighted roll and the rerolls that skip owned guns. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.feedback import ZombiesFeedback
from ....helpers import MGS_TAG
from ...common import ZombiesCommon
from .shared import owned_gun_macro_cd


# Functions
def write_mystery_box_pull() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	deny_not_enough_points: str = ZombiesCommon.deny_not_enough_points_cmd(ns, version, "#zb_mystery_box_price", f"{ns}.config")
	owned_gun_cd: str = owned_gun_macro_cd(ns)

	## Start a pull on the clicked box (@s = player, positioned at the box, #cur_box = box id)
	write_versioned_function("zombies/mystery_box/try_use", f"""
# Check if player has enough points
execute unless score @s {ns}.zb.points >= #zb_mystery_box_price {ns}.config run return run {deny_not_enough_points}

# Ensure at least a default pool exists.
function {ns}:v{version}/zombies/mystery_box/ensure_default_pool

# Deduct points, then ensure this player has a stable id so the pull display can record them as
# its buyer (set on the display below). Supports several concurrent pulls by the same player.
scoreboard players operation @s {ns}.zb.points -= #zb_mystery_box_price {ns}.config
execute unless score @s {ns}.mb.pid matches 1.. run function {ns}:v{version}/zombies/mystery_box/assign_pid

# Pre-determine if the box will move (teddy bear) — only the active box, never during a Fire Sale.
# The "after N uses, 1-in-3 chance" rule is shared with Der Wunderfizz (zombies/roaming/roll_move).
scoreboard players add #mb_pulls {ns}.data 1
scoreboard players operation #roam_uses {ns}.data = #mb_pulls {ns}.data
scoreboard players set #roam_threshold {ns}.data 4
function {ns}:v{version}/zombies/roaming/roll_move
scoreboard players operation #mb_will_move {ns}.data = #roam_will_move {ns}.data
# Gate: only the active box moves, and never during a Fire Sale
execute unless entity @n[tag=bs.interaction.target,tag={ns}.mystery_box_active] run scoreboard players set #mb_will_move {ns}.data 0
execute if score #zb_fire_sale_timer {ns}.data matches 1.. run scoreboard players set #mb_will_move {ns}.data 0
execute if score #mb_will_move {ns}.data matches 1 run scoreboard players set #mb_pulls {ns}.data 0

# Spawn the pull display here and stamp it with the box id, animation timer, and will-move flag
function {ns}:v{version}/zombies/mystery_box/spawn_display
scoreboard players operation @n[tag={ns}.mb_display_new] {ns}.mb.box = #cur_box {ns}.data
scoreboard players set @n[tag={ns}.mb_display_new] {ns}.mb.anim 105
scoreboard players operation @n[tag={ns}.mb_display_new] {ns}.mb.willmove = #mb_will_move {ns}.data
scoreboard players operation @n[tag={ns}.mb_display_new] {ns}.mb.buyer = @s {ns}.mb.pid

# Timeslip: this buyer's pull spins 2x faster
scoreboard players set @n[tag={ns}.mb_display_new] {ns}.mb.timeslip 0
execute if score @s {ns}.special.timeslip matches 1.. run scoreboard players set @n[tag={ns}.mb_display_new] {ns}.mb.timeslip 1

tag @n[tag={ns}.mb_display_new] remove {ns}.mb_display_new

# Open this box's lid + open/spin sounds + a private announce to the buyer
function {ns}:v{version}/zombies/mystery_box/open_lid
{ZombiesFeedback.zb_sound('box_open')}
# Timeslip owners get the sped-up spin tune to match their 2x pull
execute unless score @s {ns}.special.timeslip matches 1.. run {ZombiesFeedback.zb_sound('box_spin')}
execute unless score @s {ns}.special.timeslip matches 1.. run {ZombiesFeedback.zb_sound('music_box')}
execute if score @s {ns}.special.timeslip matches 1.. run {ZombiesFeedback.zb_sound('box_spin')}
execute if score @s {ns}.special.timeslip matches 1.. run {ZombiesFeedback.zb_sound('music_box_short')}
tellraw @s [{MGS_TAG},{{"text":"Mystery Box spinning...","color":"light_purple"}}]
""")

	## Assign a stable unique id to a player the first time they pull (@s = player).
	write_versioned_function("zombies/mystery_box/assign_pid", f"""
scoreboard players add #mb_pid_counter {ns}.data 1
scoreboard players operation @s {ns}.mb.pid = #mb_pid_counter {ns}.data
""")

	write_versioned_function("zombies/mystery_box/pick_random_result", f"""
execute store result score #mb_pool_size {ns}.data run data get storage {ns}:zombies mystery_box_pool
execute if score #mb_pool_size {ns}.data matches ..0 run return run function {ns}:v{version}/zombies/mystery_box/deny_pool_empty
data modify storage bs:in random.weighted_choice.options set from storage {ns}:zombies mystery_box_pool
data modify storage bs:in random.weighted_choice.weights set from storage {ns}:zombies mystery_box_weights
function #bs.random:weighted_choice
data modify storage {ns}:zombies mystery_box.result set from storage bs:out random.weighted_choice
""")

	write_versioned_function("zombies/mystery_box/check_owned_result", f"""
scoreboard players set #mb_owned {ns}.data 0
$execute if items entity @s hotbar.1 *[custom_data~{owned_gun_cd}] run scoreboard players set #mb_owned {ns}.data 1
$execute if items entity @s hotbar.2 *[custom_data~{owned_gun_cd}] run scoreboard players set #mb_owned {ns}.data 1
$execute if items entity @s hotbar.3 *[custom_data~{owned_gun_cd}] run scoreboard players set #mb_owned {ns}.data 1
# Tactical slot (monkey bombs): holding any counts as owned, so the box rerolls like duplicate guns
$execute if items entity @s hotbar.6 *[custom_data~{owned_gun_cd}] run scoreboard players set #mb_owned {ns}.data 1

# Also treat as owned if Ray Gun cap (max 2 players) is reached and result is Ray Gun (special case to limit 2 Ray Guns per game)
execute if score #mb_owned {ns}.data matches 0 run function {ns}:v{version}/zombies/mystery_box/check_ray_gun_cap
""")

	write_versioned_function("zombies/mystery_box/check_ray_gun_cap", f"""
# Only applies when the result is ray_gun
execute unless data storage {ns}:zombies mystery_box.result{{weapon_id:"ray_gun"}} run return fail

# Count ray_gun owners across all in-game players (cap = 2)
scoreboard players set #mb_ray_gun_owners {ns}.data 0
execute as @a[scores={{{ns}.zb.in_game=1}}] if items entity @s hotbar.1 *[custom_data~{{{ns}:{{gun:true,stats:{{base_weapon:"ray_gun"}}}}}}] run scoreboard players add #mb_ray_gun_owners {ns}.data 1
execute as @a[scores={{{ns}.zb.in_game=1}}] if items entity @s hotbar.2 *[custom_data~{{{ns}:{{gun:true,stats:{{base_weapon:"ray_gun"}}}}}}] run scoreboard players add #mb_ray_gun_owners {ns}.data 1
execute as @a[scores={{{ns}.zb.in_game=1}}] if items entity @s hotbar.3 *[custom_data~{{{ns}:{{gun:true,stats:{{base_weapon:"ray_gun"}}}}}}] run scoreboard players add #mb_ray_gun_owners {ns}.data 1
execute if score #mb_ray_gun_owners {ns}.data matches 2.. run scoreboard players set #mb_owned {ns}.data 1
""")

	write_versioned_function("zombies/mystery_box/reroll_owned", f"""
scoreboard players set #mb_owned {ns}.data 0
execute if data storage {ns}:zombies mystery_box.result.weapon_id run function {ns}:v{version}/zombies/mystery_box/check_owned_result with storage {ns}:zombies mystery_box.result
execute if score #mb_owned {ns}.data matches 1 if score #mb_reroll {ns}.data matches ..19 run scoreboard players add #mb_reroll {ns}.data 1
execute if score #mb_owned {ns}.data matches 1 if score #mb_reroll {ns}.data matches ..19 run function {ns}:v{version}/zombies/mystery_box/pick_random_result
execute if score #mb_owned {ns}.data matches 1 if score #mb_reroll {ns}.data matches ..19 run function {ns}:v{version}/zombies/mystery_box/reroll_owned
""")

	write_versioned_function("zombies/mystery_box/deny_pool_empty", f"""
# Clear any stale result so downstream checks treat this pull as failed
data remove storage {ns}:zombies mystery_box.result
tellraw @s [{MGS_TAG},{{"text":"The Mystery Box has no weapons available.","color":"red"}}]
{ZombiesFeedback.zb_sound('deny')}
""")

	## Display entity: spawned at box level; floats up via the per-display tick (anim==104).
	write_versioned_function("zombies/mystery_box/spawn_display", f"""
summon minecraft:item_display ~ ~-1.5 ~ {{Tags:["{ns}.mb_display","{ns}.gm_entity","{ns}.mb_display_new"],item_display:"fixed",item:{{id:"minecraft:nether_star",count:1,components:{{"minecraft:item_model":"air"}}}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.4f,0.4f,0.4f]}},billboard:"fixed"}}
tp @n[tag={ns}.mb_display_new] ~ ~-1.5 ~ ~ ~
""")

