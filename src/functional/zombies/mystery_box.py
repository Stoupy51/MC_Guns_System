
# ruff: noqa: E501
# Mystery Box System
# Dynamic weapon pool, visual animation with item cycling, random selection.
# Price: 950 points (configurable via #zb_mystery_box_price config)
# Pool can be extended via function tag #mgs:zombies/register_mystery_box_item
# Uses Bookshelf interaction module for click/hover detection.
# Positions use compound format: {pos:[x,y,z], rotation:[yaw,0.0f], group_id:N, can_start_on:1b}

from stewbeet import Mem, write_versioned_function

from ...config.catalogs import PRIMARY_WEAPONS, SECONDARY_WEAPONS
from ..helpers import MGS_TAG
from ..multiplayer.classes import CONSUMABLE_MAGS


def generate_mystery_box() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	owned_gun_macro_cd: str = "{" + ns + ':{gun:true,stats:{base_weapon:"$(weapon_id)"}}}'
	weapon_pool_meta: dict[str, tuple[str, int, bool]] = {}
	for weapon_id, _, _, mag_id, mag_count in PRIMARY_WEAPONS:
		weapon_pool_meta.setdefault(weapon_id, (mag_id, mag_count, mag_id in CONSUMABLE_MAGS))
	for weapon_id, _, mag_id, mag_count in SECONDARY_WEAPONS:
		weapon_pool_meta.setdefault(weapon_id, (mag_id, mag_count, mag_id in CONSUMABLE_MAGS))
	default_pool_weapons: tuple[str, ...] = tuple(weapon_pool_meta.keys())

	default_pool_entries: str = ",".join(
		[
			(
				f'{{weapon_id:"{weapon_id}",'
				f'give_function:"{ns}:v{version}/zombies/mystery_box/default_give/{weapon_id}",'
				f'mag_id:"{weapon_pool_meta[weapon_id][0]}",'
				f'mag_count:{weapon_pool_meta[weapon_id][1]},'
				f'consumable:{"1b" if weapon_pool_meta[weapon_id][2] else "0b"}}}'
			)
			for weapon_id in default_pool_weapons
		]
	)

	for weapon_id in default_pool_weapons:
		mag_id, mag_count, is_consumable = weapon_pool_meta[weapon_id]
		write_versioned_function(f"zombies/mystery_box/default_give/{weapon_id}", f"""
data modify storage {ns}:temp _wb_weapon set value {{weapon_id:"{weapon_id}",name:"{weapon_id}",consumable:{"1b" if is_consumable else "0b"},mag_id:"{mag_id}",mag_count:{mag_count}}}
scoreboard players set #wb_price {ns}.data 0
function {ns}:v{version}/zombies/wallbuys/process_purchase with storage {ns}:temp _wb_weapon
execute if score #wb_purchase_done {ns}.data matches 1 if data storage {ns}:temp _wb_weapon{{consumable:1b}} run function {ns}:v{version}/zombies/mystery_box/give_consumable_reserve with storage {ns}:temp _wb_weapon
""")

	write_versioned_function("zombies/mystery_box/give_consumable_reserve", f"""
scoreboard players set #mb_mag_given {ns}.data 0

$execute if score #mb_mag_given {ns}.data matches 0 if items entity @s hotbar.1 *[custom_data~{owned_gun_macro_cd}] run function {ns}:v{version}/zombies/mystery_box/give_consumable_slot {{inventory:1,mag_id:"$(mag_id)",mag_count:$(mag_count)}}
$execute if score #mb_mag_given {ns}.data matches 0 if items entity @s hotbar.2 *[custom_data~{owned_gun_macro_cd}] run function {ns}:v{version}/zombies/mystery_box/give_consumable_slot {{inventory:2,mag_id:"$(mag_id)",mag_count:$(mag_count)}}
$execute if score #mb_mag_given {ns}.data matches 0 if items entity @s hotbar.3 *[custom_data~{owned_gun_macro_cd}] run function {ns}:v{version}/zombies/mystery_box/give_consumable_slot {{inventory:3,mag_id:"$(mag_id)",mag_count:$(mag_count)}}
""")

	write_versioned_function("zombies/mystery_box/give_consumable_slot", f"""
$loot replace entity @s inventory.$(inventory) loot {ns}:i/$(mag_id)
$scoreboard players set #bullets {ns}.data $(mag_count)
$item modify entity @s inventory.$(inventory) {ns}:v{version}/set_consumable_count
$function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"inventory.$(inventory)",group:"inventory",index:$(inventory)}}
scoreboard players set #mb_mag_given {ns}.data 1
""")

	write_versioned_function("zombies/mystery_box/ensure_default_pool", f"""
data modify storage {ns}:zombies mystery_box_pool set value [{default_pool_entries}]
""")

	## Setup: iterate mystery box position compounds, summon interaction entities with Bookshelf
	write_versioned_function("zombies/mystery_box/setup_positions", f"""
# Summon mystery box markers at map positions
data modify storage {ns}:temp _mb_iter set from storage {ns}:zombies game.map.mystery_box.positions
execute if data storage {ns}:temp _mb_iter[0] run function {ns}:v{version}/zombies/mystery_box/setup_pos_iter

# Pick a random position with can_start_on as the active mystery box
execute as @n[tag={ns}.mystery_box_pos,tag={ns}.mb_can_start,sort=random] run tag @s add {ns}.mystery_box_active
# Fallback if no can_start_on positions exist
execute unless entity @e[tag={ns}.mystery_box_active] as @n[tag={ns}.mystery_box_pos,sort=random] run tag @s add {ns}.mystery_box_active
""")

	write_versioned_function("zombies/mystery_box/setup_pos_iter", f"""
# Read relative position from compound and convert to absolute
execute store result score #mbx {ns}.data run data get storage {ns}:temp _mb_iter[0].pos[0]
execute store result score #mby {ns}.data run data get storage {ns}:temp _mb_iter[0].pos[1]
execute store result score #mbz {ns}.data run data get storage {ns}:temp _mb_iter[0].pos[2]

scoreboard players operation #mbx {ns}.data += #gm_base_x {ns}.data
scoreboard players operation #mby {ns}.data += #gm_base_y {ns}.data
scoreboard players operation #mbz {ns}.data += #gm_base_z {ns}.data

execute store result storage {ns}:temp _mbpos.x double 1 run scoreboard players get #mbx {ns}.data
execute store result storage {ns}:temp _mbpos.y double 1 run scoreboard players get #mby {ns}.data
execute store result storage {ns}:temp _mbpos.z double 1 run scoreboard players get #mbz {ns}.data
data modify storage {ns}:temp _mbpos.rotation set from storage {ns}:temp _mb_iter[0].rotation

function {ns}:v{version}/zombies/mystery_box/summon_pos_at with storage {ns}:temp _mbpos

# Tag entities that can_start_on
data modify storage {ns}:temp can_start_on set from storage {ns}:temp _mb_iter[0].can_start_on
execute if data storage {ns}:temp {{can_start_on:1b}} run tag @n[tag={ns}.mb_new] add {ns}.mb_can_start

# Register Bookshelf events on newly spawned entity
execute as @n[tag={ns}.mb_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/mystery_box/on_right_click",executor:"source"}}
execute as @n[tag={ns}.mb_new] run function #bs.interaction:on_hover {{run:"function {ns}:v{version}/zombies/mystery_box/on_hover",executor:"source"}}
tag @n[tag={ns}.mb_new] remove {ns}.mb_new

data remove storage {ns}:temp _mb_iter[0]
execute if data storage {ns}:temp _mb_iter[0] run function {ns}:v{version}/zombies/mystery_box/setup_pos_iter
""")

	write_versioned_function("zombies/mystery_box/summon_pos_at", f"""
$summon minecraft:interaction $(x) $(y) $(z) {{width:1.5f,height:2.0f,response:true,Rotation:$(rotation),Tags:["{ns}.mystery_box_pos","{ns}.gm_entity","{ns}.mb_new","bs.entity.interaction"]}}
""")

	## On right-click: Bookshelf callback (executor:"source" = @s is the player)
	write_versioned_function("zombies/mystery_box/on_right_click", f"""
# Only respond if this is the active mystery box
execute unless entity @e[tag=bs.interaction.target,tag={ns}.mystery_box_active] run return fail

# Check game is active
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail

# If result is ready: collect
execute if data storage {ns}:zombies mystery_box{{ready:true}} run return run function {ns}:v{version}/zombies/mystery_box/collect

# If already spinning: inform player
execute if data storage {ns}:zombies mystery_box{{spinning:true}} run return run function {ns}:v{version}/zombies/mystery_box/deny_already_in_use

# Otherwise: try to use (buy)
function {ns}:v{version}/zombies/mystery_box/try_use
""")

	write_versioned_function("zombies/mystery_box/deny_already_in_use", f"""
tellraw @s [{MGS_TAG},{{"text":"Mystery Box is already in use.","color":"red"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

	write_versioned_function("zombies/mystery_box/try_use", f"""
# Check if player has enough points
execute unless score @s {ns}.zb.points >= #zb_mystery_box_price {ns}.config run return run function {ns}:v{version}/zombies/mystery_box/deny_not_enough_points

# Ensure at least a default pool exists.
function {ns}:v{version}/zombies/mystery_box/ensure_default_pool

# Deduct points
scoreboard players operation @s {ns}.zb.points -= #zb_mystery_box_price {ns}.config

# Start spinning
data modify storage {ns}:zombies mystery_box.spinning set value true

# Pick a random weapon from the pool and reroll if player already owns it.
function {ns}:v{version}/zombies/mystery_box/pick_random_result
scoreboard players set #mb_reroll {ns}.data 0
function {ns}:v{version}/zombies/mystery_box/reroll_owned

# If still owned after rerolls, refund and fail.
execute if score #mb_owned {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.points += #zb_mystery_box_price {ns}.config
execute if score #mb_owned {ns}.data matches 1 run return run function {ns}:v{version}/zombies/mystery_box/deny_all_owned

# Start animation timer (120 ticks cycling with slowdown + 150 ticks display window)
scoreboard players set #mb_anim_timer {ns}.data 120

# Spawn display entity at box position
execute at @n[tag={ns}.mystery_box_active] run function {ns}:v{version}/zombies/mystery_box/spawn_display

# Announce
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Mystery Box spinning...","color":"light_purple"}}]
function {ns}:v{version}/zombies/feedback/sound_box_spin
""")

	write_versioned_function("zombies/mystery_box/pick_random_result", f"""
execute store result score #mb_pool_size {ns}.data run data get storage {ns}:zombies mystery_box_pool
execute if score #mb_pool_size {ns}.data matches ..0 run return run function {ns}:v{version}/zombies/mystery_box/deny_pool_empty
execute store result score #mb_pick {ns}.data run random value 0..1000000
scoreboard players operation #mb_pick {ns}.data %= #mb_pool_size {ns}.data
data modify storage {ns}:temp _mb_pool_iter set from storage {ns}:zombies mystery_box_pool
function {ns}:v{version}/zombies/mystery_box/pick_item
data modify storage {ns}:zombies mystery_box.result set from storage {ns}:temp _mb_pool_iter[0]
""")

	write_versioned_function("zombies/mystery_box/check_owned_result", f"""
scoreboard players set #mb_owned {ns}.data 0
$execute if items entity @s hotbar.1 *[custom_data~{owned_gun_macro_cd}] run scoreboard players set #mb_owned {ns}.data 1
$execute if items entity @s hotbar.2 *[custom_data~{owned_gun_macro_cd}] run scoreboard players set #mb_owned {ns}.data 1
$execute if items entity @s hotbar.3 *[custom_data~{owned_gun_macro_cd}] run scoreboard players set #mb_owned {ns}.data 1
""")

	write_versioned_function("zombies/mystery_box/reroll_owned", f"""
scoreboard players set #mb_owned {ns}.data 0
execute if data storage {ns}:zombies mystery_box.result.weapon_id run function {ns}:v{version}/zombies/mystery_box/check_owned_result with storage {ns}:zombies mystery_box.result
execute if score #mb_owned {ns}.data matches 1 if score #mb_reroll {ns}.data matches ..19 run scoreboard players add #mb_reroll {ns}.data 1
execute if score #mb_owned {ns}.data matches 1 if score #mb_reroll {ns}.data matches ..19 run function {ns}:v{version}/zombies/mystery_box/pick_random_result
execute if score #mb_owned {ns}.data matches 1 if score #mb_reroll {ns}.data matches ..19 run function {ns}:v{version}/zombies/mystery_box/reroll_owned
""")

	write_versioned_function("zombies/mystery_box/deny_not_enough_points", f"""
tellraw @s [{MGS_TAG},{{"text":"You don't have enough points (","color":"red"}},{{"score":{{"name":"#zb_mystery_box_price","objective":"{ns}.config"}},"color":"yellow"}},{{"text":" needed).","color":"red"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

	write_versioned_function("zombies/mystery_box/deny_pool_empty", f"""
tellraw @s [{MGS_TAG},{{"text":"Mystery Box pool is empty.","color":"red"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

	write_versioned_function("zombies/mystery_box/deny_all_owned", f"""
tellraw @s [{MGS_TAG},{{"text":"You already own all available Mystery Box weapons. Points refunded.","color":"yellow"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

	write_versioned_function("zombies/mystery_box/pick_item", f"""
execute if score #mb_pick {ns}.data matches 1.. run data remove storage {ns}:temp _mb_pool_iter[0]
execute if score #mb_pick {ns}.data matches 1.. run scoreboard players remove #mb_pick {ns}.data 1
execute if score #mb_pick {ns}.data matches 1.. run function {ns}:v{version}/zombies/mystery_box/pick_item
""")

	## Display entity: spawns at box level, floats up with interpolation
	write_versioned_function("zombies/mystery_box/spawn_display", f"""
# Spawn item display at box level with small scale and correct facing
summon minecraft:item_display ~ ~0.5 ~ {{Tags:["{ns}.mb_display","{ns}.gm_entity","{ns}.mb_display_new"],item_display:"fixed",item:{{id:"minecraft:nether_star",count:1,components:{{"minecraft:item_model":"air"}}}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.5f,0.5f,0.5f]}},billboard:"fixed"}}
tp @n[tag={ns}.mb_display_new] ~ ~0.5 ~ ~ ~

# Apply interpolation a few ticks later to avoid same-tick spawn interpolation glitches.
schedule function {ns}:v{version}/zombies/mystery_box/spawn_display_finalize 5t append
""")

	write_versioned_function("zombies/mystery_box/spawn_display_finalize", f"""
data merge entity @n[tag={ns}.mb_display_new] {{transformation:{{translation:[0f,0.8f,0f]}},start_interpolation:0,interpolation_duration:200}}
tag @n[tag={ns}.mb_display_new] remove {ns}.mb_display_new
""")

	## Mystery box tick: handle animation
	write_versioned_function("zombies/mystery_box/tick", f"""
# Only tick if spinning
execute unless data storage {ns}:zombies mystery_box{{spinning:true}} run return 0

# Decrement timer
scoreboard players remove #mb_anim_timer {ns}.data 1

# Cycling phase (timer > 0): show random items with staged slowdown cadence
execute if score #mb_anim_timer {ns}.data matches 1.. run function {ns}:v{version}/zombies/mystery_box/cycle_step

# Landing phase (timer = 0): show the result
execute if score #mb_anim_timer {ns}.data matches 0 run function {ns}:v{version}/zombies/mystery_box/show_result

# Pickup window expired (timer = -150): remove display and reset
execute if score #mb_anim_timer {ns}.data matches ..-150 run function {ns}:v{version}/zombies/mystery_box/reset
""")

	write_versioned_function("zombies/mystery_box/cycle_step", f"""
# elapsed = 80 - timer
scoreboard players set #mb_elapsed {ns}.data 80
scoreboard players operation #mb_elapsed {ns}.data -= #mb_anim_timer {ns}.data

# Constants for modulo cadence checks
scoreboard players set #mb_c2 {ns}.data 2
scoreboard players set #mb_c5 {ns}.data 5
scoreboard players set #mb_c8 {ns}.data 8

# 0..29 ticks elapsed: every 2 ticks
scoreboard players operation #mb_mod {ns}.data = #mb_elapsed {ns}.data
execute if score #mb_elapsed {ns}.data matches ..29 run scoreboard players operation #mb_mod {ns}.data %= #mb_c2 {ns}.data
execute if score #mb_elapsed {ns}.data matches ..29 if score #mb_mod {ns}.data matches 0 run function {ns}:v{version}/zombies/mystery_box/cycle_display

# 30..49 ticks elapsed: every 5 ticks
scoreboard players operation #mb_mod {ns}.data = #mb_elapsed {ns}.data
execute if score #mb_elapsed {ns}.data matches 30..49 run scoreboard players operation #mb_mod {ns}.data %= #mb_c5 {ns}.data
execute if score #mb_elapsed {ns}.data matches 30..49 if score #mb_mod {ns}.data matches 0 run function {ns}:v{version}/zombies/mystery_box/cycle_display

# 50+ ticks elapsed: every 8 ticks
scoreboard players operation #mb_mod {ns}.data = #mb_elapsed {ns}.data
execute if score #mb_elapsed {ns}.data matches 50.. run scoreboard players operation #mb_mod {ns}.data %= #mb_c8 {ns}.data
execute if score #mb_elapsed {ns}.data matches 50.. if score #mb_mod {ns}.data matches 0 run function {ns}:v{version}/zombies/mystery_box/cycle_display
""")

	## Cycle display: swap the item_display model to simulate cycling
	write_versioned_function("zombies/mystery_box/cycle_display", f"""
# Pick a random item from pool to display
execute store result score #mb_cycle {ns}.data run random value 0..100
execute store result score #mb_ps {ns}.data run data get storage {ns}:zombies mystery_box_pool
scoreboard players operation #mb_cycle {ns}.data %= #mb_ps {ns}.data

data modify storage {ns}:temp _mb_cycle_iter set from storage {ns}:zombies mystery_box_pool
function {ns}:v{version}/zombies/mystery_box/cycle_iterate

# Apply the cycled item to the display entity.
execute if data storage {ns}:temp _mb_cycle_iter[0].weapon_id run function {ns}:v{version}/zombies/mystery_box/cycle_display_weapon with storage {ns}:temp _mb_cycle_iter[0]
execute unless data storage {ns}:temp _mb_cycle_iter[0].weapon_id run data modify entity @n[tag={ns}.mb_display] item set from storage {ns}:temp _mb_cycle_iter[0].display_item
""")

	write_versioned_function("zombies/mystery_box/cycle_display_weapon", f"""
$loot replace entity @n[tag={ns}.mb_display] contents loot {ns}:i/$(weapon_id)
""")

	write_versioned_function("zombies/mystery_box/cycle_iterate", f"""
execute if score #mb_cycle {ns}.data matches 1.. run data remove storage {ns}:temp _mb_cycle_iter[0]
execute if score #mb_cycle {ns}.data matches 1.. run scoreboard players remove #mb_cycle {ns}.data 1
execute if score #mb_cycle {ns}.data matches 1.. run function {ns}:v{version}/zombies/mystery_box/cycle_iterate
""")

	## Show result: display the final picked weapon with interpolation
	write_versioned_function("zombies/mystery_box/show_result", f"""
# Set display to final result
execute if data storage {ns}:zombies mystery_box.result.weapon_id run function {ns}:v{version}/zombies/mystery_box/show_result_weapon with storage {ns}:zombies mystery_box.result
execute unless data storage {ns}:zombies mystery_box.result.weapon_id run data modify entity @n[tag={ns}.mb_display] item set from storage {ns}:zombies mystery_box.result.display_item

# Start at y=1.5, then descend to y=0.0 over 7.5s (150 ticks)
data merge entity @n[tag={ns}.mb_display] {{transformation:{{translation:[0f,1.5f,0f]}}}}
data merge entity @n[tag={ns}.mb_display] {{interpolation_duration:150,transformation:{{translation:[0f,0f,0f]}},start_interpolation:0}}

# Tag the box as ready for pickup
data modify storage {ns}:zombies mystery_box.ready set value true

# Announce result
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Mystery Box result ready! ","color":"light_purple"}},{{"text":"Right-click to collect!","color":"green","bold":true}}]
function {ns}:v{version}/zombies/feedback/sound_box_ready
""")

	write_versioned_function("zombies/mystery_box/show_result_weapon", f"""
$loot replace entity @n[tag={ns}.mb_display] contents loot {ns}:i/$(weapon_id)
""")

	## Collect the mystery box result (called from on_right_click, @s = player)
	write_versioned_function("zombies/mystery_box/collect", f"""
# Give the result item to the player via its give function
scoreboard players set #wb_purchase_done {ns}.data 0
scoreboard players set #wb_purchase_mode {ns}.data -1
execute if data storage {ns}:zombies mystery_box.result.give_function run function {ns}:v{version}/zombies/mystery_box/give_via_function

# If the give flow failed (e.g. invalid selected slot), keep result ready for retry.
execute if score #wb_purchase_done {ns}.data matches 0 run return 0

# Resolve the collected weapon display name from the given item.
execute if data storage {ns}:zombies mystery_box.result.weapon_id run function {ns}:v{version}/zombies/mystery_box/capture_collected_name with storage {ns}:zombies mystery_box.result

# Announce
tellraw @s [{MGS_TAG},{{"text":"You collected ","color":"green"}},{{"storage":"{ns}:temp","nbt":"_mb_collected_name","interpret":true}},{{"text":" from the Mystery Box.","color":"green"}}]
function {ns}:v{version}/zombies/feedback/sound_success

# Reset box
function {ns}:v{version}/zombies/mystery_box/reset
""")

	write_versioned_function("zombies/mystery_box/capture_collected_name", f"""
data modify storage {ns}:temp _mb_collected_name set value [{{"text":"$(weapon_id)","color":"gold"}}]
scoreboard players set #mb_name_found {ns}.data 0

$execute if score #mb_name_found {ns}.data matches 0 if items entity @s hotbar.1 *[custom_data~{owned_gun_macro_cd}] run function {ns}:v{version}/zombies/mystery_box/capture_collected_name_slot {{slot:"hotbar.1"}}
$execute if score #mb_name_found {ns}.data matches 0 if items entity @s hotbar.2 *[custom_data~{owned_gun_macro_cd}] run function {ns}:v{version}/zombies/mystery_box/capture_collected_name_slot {{slot:"hotbar.2"}}
$execute if score #mb_name_found {ns}.data matches 0 if items entity @s hotbar.3 *[custom_data~{owned_gun_macro_cd}] run function {ns}:v{version}/zombies/mystery_box/capture_collected_name_slot {{slot:"hotbar.3"}}
""")

	write_versioned_function("zombies/mystery_box/capture_collected_name_slot", f"""
tag @s add {ns}.mb_name_reader
$execute summon item_display run function {ns}:v{version}/zombies/mystery_box/extract_collected_item_name {{slot:"$(slot)"}}
tag @s remove {ns}.mb_name_reader
scoreboard players set #mb_name_found {ns}.data 1
""")

	write_versioned_function("zombies/mystery_box/extract_collected_item_name", f"""
$item replace entity @s contents from entity @p[tag={ns}.mb_name_reader] $(slot)
data modify storage {ns}:temp _mb_collected_name set from entity @s item.components."minecraft:item_name"
kill @s
""")

	write_versioned_function("zombies/mystery_box/give_via_function", f"""
function {ns}:v{version}/zombies/mystery_box/run_give with storage {ns}:zombies mystery_box.result
""")

	write_versioned_function("zombies/mystery_box/run_give", """
$function $(give_function)
""")

	## Reset mystery box state
	write_versioned_function("zombies/mystery_box/reset", f"""
# Kill display entity
kill @e[tag={ns}.mb_display]

# Reset state
data modify storage {ns}:zombies mystery_box.spinning set value false
data modify storage {ns}:zombies mystery_box.ready set value false
data remove storage {ns}:zombies mystery_box.result
""")

	## Hover functions for active mystery box
	write_versioned_function("zombies/mystery_box/hud_ready", """
data modify storage smithed.actionbar:input message set value {json:[{"text":"🎲 Mystery Box","color":"light_purple"},{"text":" - ","color":"gray"},{"text":"Click to collect!","color":"green"}],priority:'notification',freeze:5}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/mystery_box/hud_spinning", """
data modify storage smithed.actionbar:input message set value {json:[{"text":"🎲 Mystery Box","color":"light_purple"},{"text":" - ","color":"gray"},{"text":"Spinning...","color":"yellow"}],priority:'notification',freeze:5}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/mystery_box/hud_price", """
data modify storage smithed.actionbar:input message set value {json:[{"text":"🎲 Mystery Box","color":"light_purple"},{"text":" - ","color":"gray"},{"text":"950 points","color":"gold"}],priority:'notification',freeze:5}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/mystery_box/on_hover", f"""
execute unless entity @e[tag=bs.interaction.target,tag={ns}.mystery_box_active] run return fail
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail
execute if data storage {ns}:zombies mystery_box{{ready:true}} run return run function {ns}:v{version}/zombies/mystery_box/hud_ready
execute if data storage {ns}:zombies mystery_box{{spinning:true}} run return run function {ns}:v{version}/zombies/mystery_box/hud_spinning
function {ns}:v{version}/zombies/mystery_box/hud_price
""")

	## Hook into game tick for mystery box animation only (interaction handled by Bookshelf)
	write_versioned_function("zombies/game_tick", f"""
# Mystery box animation tick
function {ns}:v{version}/zombies/mystery_box/tick
""")

	## Hook into game start to setup mystery box positions
	write_versioned_function("zombies/preload_complete", f"""
# Setup mystery box positions
execute if data storage {ns}:zombies game.map.mystery_box.positions[0] run function {ns}:v{version}/zombies/mystery_box/setup_positions
""")

	## Hook into stop to reset mystery box
	write_versioned_function("zombies/stop", f"""
# Reset mystery box
function {ns}:v{version}/zombies/mystery_box/reset
""")
