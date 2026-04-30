
# ruff: noqa: E501
# Mystery Box System
# Dynamic weapon pool, visual animation with item cycling, random selection.
# Price: 950 points (configurable via #zb_mystery_box_price config)
# Pool can be extended via function tag #mgs:zombies/register_mystery_box_item
# Uses Bookshelf interaction module for click/hover detection.
# Positions use compound format: {pos:[x,y,z], rotation:[yaw,0.0f], group_id:N, can_start_on:1b}
from stewbeet import LootTable, Mem, set_json_encoder, write_versioned_function

from ...config.stats import WEIGHT
from ...database.weapons import WEAPON_STATS
from ..helpers import MGS_TAG
from .common import build_weapon_magazine_data

# Move animation constants
MOVE_BEAR_TICKS: int = 30		# bear visible before ascend starts
MOVE_ASCEND_TICKS: int = 80	# ascend at old location
MOVE_WAIT_TICKS: int = 100		# 5-second wait before descending
MOVE_DESCEND_TICKS: int = 70	# descend at new location
MOVE_TOTAL_TICKS: int = MOVE_BEAR_TICKS + MOVE_ASCEND_TICKS + MOVE_WAIT_TICKS + MOVE_DESCEND_TICKS	# 280

# Teddy bear player head texture (Black Ops easter egg)
BEAR_HEAD_TEXTURE: str = "eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvY2RiNjZjZjlmMTdlMTQ4OTMxMGM3YWNjNjgxMDE2MDUxMTk2YTg0OGUwNzZkYjZmYzA5MzkxYjkyODcyYTc3NyJ9fX0="


def generate_mystery_box() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	owned_gun_macro_cd: str = "{" + ns + ':{gun:true,stats:{base_weapon:"$(weapon_id)"}}}'

	# Register teddy bear loot table for Mystery Box move animation
	Mem.ctx.data[ns].loot_tables["zombies/mystery_box_bear"] = set_json_encoder(LootTable({
		"pools": [{
			"rolls": 1,
			"entries": [{
				"type": "minecraft:item",
				"name": "minecraft:player_head",
				"functions": [{
					"function": "minecraft:set_components",
					"components": {
						"minecraft:profile": {
							"properties": [{
								"name": "textures",
								"value": BEAR_HEAD_TEXTURE,
							}],
						},
					},
				}],
			}],
		}],
	}))

	# Use common helper to build weapon->magazine mappings from catalogs
	weapon_mag_data: dict[str, tuple[str, int, bool]] = build_weapon_magazine_data()
	default_pool_weapons: tuple[str, ...] = tuple(weapon_mag_data.keys())

	pool_entries: list[str] = []
	pool_weights: list[int] = []
	for weapon_id in default_pool_weapons:
		weight: int = WEAPON_STATS.get(weapon_id, {}).get("stats", {}).get(WEIGHT, 5)
		if weight == 0:
			continue  # Weight 0 = excluded from mystery box
		mag_id, mag_count, is_consumable = weapon_mag_data[weapon_id]
		pool_entries.append(
			f'{{weapon_id:"{weapon_id}",'
			f'give_function:"{ns}:v{version}/zombies/mystery_box/default_give/{weapon_id}",'
			f'magazine_id:"{mag_id}",'
			f'mag_count:{mag_count},'
			f'consumable:{"1b" if is_consumable else "0b"}}}'
		)
		pool_weights.append(weight)
	default_pool_entries: str = ",".join(pool_entries)
	default_pool_weights: str = ",".join(str(w) for w in pool_weights)

	for weapon_id in default_pool_weapons:
		magazine_id, mag_count, is_consumable = weapon_mag_data[weapon_id]
		write_versioned_function(f"zombies/mystery_box/default_give/{weapon_id}", f"""
data modify storage {ns}:temp _wb_weapon set value {{weapon_id:"{weapon_id}",name:"{weapon_id}",consumable:{"1b" if is_consumable else "0b"},magazine_id:"{magazine_id}",mag_count:{mag_count}}}
scoreboard players set #wb_price {ns}.data 0
function {ns}:v{version}/zombies/wallbuys/process_purchase with storage {ns}:temp _wb_weapon
""")

	write_versioned_function("zombies/mystery_box/ensure_default_pool", f"""
data modify storage {ns}:zombies mystery_box_pool set value [{default_pool_entries}]
data modify storage {ns}:zombies mystery_box_weights set value [{default_pool_weights}]
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

# Init pull counter and spawn presence chest at the active position.
scoreboard players set #mb_pulls {ns}.data 0
function {ns}:v{version}/zombies/mystery_box/sync_presence_display
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

	write_versioned_function("zombies/mystery_box/sync_presence_display", f"""
# Keep one chest display at the currently active mystery box.
kill @e[tag={ns}.mb_presence]
execute as @n[tag={ns}.mystery_box_active] at @s run data modify storage {ns}:temp _mb_chest.yaw set value 0.0f
execute as @n[tag={ns}.mystery_box_active] at @s run data modify storage {ns}:temp _mb_chest.yaw set from entity @s Rotation[0]
execute as @n[tag={ns}.mystery_box_active] at @s run function {ns}:v{version}/zombies/mystery_box/summon_presence_display with storage {ns}:temp _mb_chest
""")

	write_versioned_function("zombies/mystery_box/summon_presence_display", f"""
$execute positioned ~ ~0.7 ~ run summon minecraft:item_display ~ ~ ~ {{Rotation:[$(yaw),0f],Tags:["{ns}.mb_presence","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:chest",count:1}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.85f,0.85f,0.85f]}}}}
""")

	write_versioned_function("zombies/mystery_box/move_active_position", f"""
# Need at least 2 positions to move.
execute store result score #mb_pos_count {ns}.data run data get storage {ns}:zombies game.map.mystery_box.positions
execute if score #mb_pos_count {ns}.data matches ..1 run return 0

tag @e[tag={ns}.mystery_box_active] add {ns}.mb_prev_active
tag @e[tag={ns}.mystery_box_active] remove {ns}.mystery_box_active
execute as @n[tag={ns}.mystery_box_pos,tag=!{ns}.mb_prev_active,sort=random] run tag @s add {ns}.mystery_box_active
tag @e[tag={ns}.mb_prev_active] remove {ns}.mb_prev_active
""")

	## On right-click: Bookshelf callback (executor:"source" = @s is the player)
	write_versioned_function("zombies/mystery_box/on_right_click", f"""
# Only respond if this is the active mystery box
execute unless entity @e[tag=bs.interaction.target,tag={ns}.mystery_box_active] run return fail

# Check game is active
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail

# If box is moving: deny
execute if score #mb_move_timer {ns}.data matches 1.. run return run function {ns}:v{version}/zombies/mystery_box/deny_moving

# If result is ready: only the buyer can collect
execute if data storage {ns}:zombies mystery_box{{ready:true}} if entity @s[tag={ns}.mb_buyer] run return run function {ns}:v{version}/zombies/mystery_box/collect
execute if data storage {ns}:zombies mystery_box{{ready:true}} unless entity @s[tag={ns}.mb_buyer] run return run function {ns}:v{version}/zombies/mystery_box/deny_not_your_result

# If already spinning: inform player
execute if data storage {ns}:zombies mystery_box{{spinning:true}} run return run function {ns}:v{version}/zombies/mystery_box/deny_already_in_use

# Otherwise: try to use (buy)
function {ns}:v{version}/zombies/mystery_box/try_use
""")

	write_versioned_function("zombies/mystery_box/deny_moving", f"""
tellraw @s [{MGS_TAG},{{"text":"The Mystery Box is moving...","color":"yellow"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
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

# Tag buyer for potential bear-result refund
tag @s add {ns}.mb_buyer

# Pre-determine if box will move (replaces maybe_move_after_pull)
scoreboard players set #mb_will_move {ns}.data 0
scoreboard players add #mb_pulls {ns}.data 1
execute if score #mb_pulls {ns}.data matches 4.. store result score #mb_move_roll {ns}.data run random value 0..2
execute if score #mb_pulls {ns}.data matches 4.. if score #mb_move_roll {ns}.data matches 0 run scoreboard players set #mb_will_move {ns}.data 1
execute if score #mb_will_move {ns}.data matches 1 run scoreboard players set #mb_pulls {ns}.data 0

# Start spinning
data modify storage {ns}:zombies mystery_box.spinning set value true

# Pick a random weapon from the pool and reroll if player already owns it.
function {ns}:v{version}/zombies/mystery_box/pick_random_result
scoreboard players set #mb_reroll {ns}.data 0
function {ns}:v{version}/zombies/mystery_box/reroll_owned

# If still owned after rerolls, refund and fail.
execute if score #mb_owned {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.points += #zb_mystery_box_price {ns}.config
execute if score #mb_owned {ns}.data matches 1 run tag @s remove {ns}.mb_buyer
execute if score #mb_owned {ns}.data matches 1 run return run function {ns}:v{version}/zombies/mystery_box/deny_all_owned

# Start animation timer (100 ticks cycling with slowdown + 150 ticks display window)
scoreboard players set #mb_anim_timer {ns}.data 105

# Spawn display entity at box position
execute at @n[tag={ns}.mystery_box_active] run function {ns}:v{version}/zombies/mystery_box/spawn_display

# Announce
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"Mystery Box spinning...","color":"light_purple"}}]
execute as @n[tag={ns}.mystery_box_active] at @s run function {ns}:v{version}/zombies/feedback/sound_box_open
execute as @n[tag={ns}.mystery_box_active] at @s run function {ns}:v{version}/zombies/feedback/sound_box_spin
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
$execute if items entity @s hotbar.1 *[custom_data~{owned_gun_macro_cd}] run scoreboard players set #mb_owned {ns}.data 1
$execute if items entity @s hotbar.2 *[custom_data~{owned_gun_macro_cd}] run scoreboard players set #mb_owned {ns}.data 1
$execute if items entity @s hotbar.3 *[custom_data~{owned_gun_macro_cd}] run scoreboard players set #mb_owned {ns}.data 1

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

	write_versioned_function("zombies/mystery_box/deny_not_enough_points", f"""
tellraw @s [{MGS_TAG},{{"text":"You don't have enough points (","color":"red"}},{{"score":{{"name":"#zb_mystery_box_price","objective":"{ns}.config"}},"color":"yellow"}},{{"text":" needed).","color":"red"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

	write_versioned_function("zombies/mystery_box/deny_not_your_result", f"""
tellraw @s [{MGS_TAG},{{"text":"Wait for the current player to collect their result.","color":"red"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

	write_versioned_function("zombies/mystery_box/deny_all_owned", f"""
tellraw @s [{MGS_TAG},{{"text":"You already own all available Mystery Box weapons. Points refunded.","color":"yellow"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
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
# Spin animation tick
execute if data storage {ns}:zombies mystery_box{{spinning:true}} run function {ns}:v{version}/zombies/mystery_box/spin_tick

# Move animation tick (independent of spin)
execute if score #mb_move_timer {ns}.data matches 1.. run function {ns}:v{version}/zombies/mystery_box/move_anim_tick
""")

	write_versioned_function("zombies/mystery_box/spin_tick", f"""
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
data modify storage bs:in random.weighted_choice.options set from storage {ns}:zombies mystery_box_pool
data modify storage bs:in random.weighted_choice.weights set from storage {ns}:zombies mystery_box_weights
function #bs.random:weighted_choice
data modify storage {ns}:temp _mb_cycle_item set from storage bs:out random.weighted_choice

# Apply the cycled item to the display entity.
execute if data storage {ns}:temp _mb_cycle_item.weapon_id run function {ns}:v{version}/zombies/mystery_box/cycle_display_weapon with storage {ns}:temp _mb_cycle_item
execute unless data storage {ns}:temp _mb_cycle_item.weapon_id run data modify entity @n[tag={ns}.mb_display] item set from storage {ns}:temp _mb_cycle_item.display_item
""")

	write_versioned_function("zombies/mystery_box/cycle_display_weapon", f"""
$loot replace entity @n[tag={ns}.mb_display] contents loot {ns}:i/$(weapon_id)
""")



	## Show result: display the final picked weapon with interpolation
	write_versioned_function("zombies/mystery_box/show_result", f"""
# If box will move, show teddy bear instead of weapon
execute if score #mb_will_move {ns}.data matches 1 run return run function {ns}:v{version}/zombies/mystery_box/show_bear_result

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
""")

	write_versioned_function("zombies/mystery_box/show_result_weapon", f"""
$loot replace entity @n[tag={ns}.mb_display] contents loot {ns}:i/$(weapon_id)
""")

	## Teddy bear result: box is about to move (Black Ops style)
	write_versioned_function("zombies/mystery_box/show_bear_result", f"""
# Replace display with teddy bear
loot replace entity @n[tag={ns}.mb_display] contents loot {ns}:zombies/mystery_box_bear

# Rise bear out of the box (like normal result)
data merge entity @n[tag={ns}.mb_display] {{transformation:{{translation:[0f,1.5f,0f]}}}}
data merge entity @n[tag={ns}.mb_display] {{interpolation_duration:40,transformation:{{translation:[0f,0.5f,0f]}},start_interpolation:0}}

# Refund the buyer
execute as @a[tag={ns}.mb_buyer] run scoreboard players operation @s {ns}.zb.points += #zb_mystery_box_price {ns}.config
tag @a[tag={ns}.mb_buyer] remove {ns}.mb_buyer

# Stop spin, start move animation timer
data modify storage {ns}:zombies mystery_box.spinning set value false
scoreboard players set #mb_move_timer {ns}.data {MOVE_TOTAL_TICKS}

# Announce
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"The Mystery Box is moving!","color":"yellow","bold":true}}]
execute as @n[tag={ns}.mystery_box_active] at @s run function {ns}:v{version}/zombies/feedback/sound_box_bye_bye
""")

	## Move animation: tick dispatcher
	# Timer phases (counting down from {MOVE_TOTAL_TICKS}=280):
	#   bear visible (280..251): bear rises out of box (30 ticks)
	#   ascend (250..171): chest + bear rise up (80 ticks)
	#   wait (170..71): pause with no box visible (100 ticks = 5 seconds)
	#   transition (70): pick new location, spawn descending chest
	#   descend (69..1): chest descends at new location (69 ticks)
	#   land (0): finalize

	ascend_start: int = MOVE_ASCEND_TICKS + MOVE_WAIT_TICKS + MOVE_DESCEND_TICKS + 1	# 251
	ascend_end: int = MOVE_WAIT_TICKS + MOVE_DESCEND_TICKS + 1						# 171
	transition: int = MOVE_DESCEND_TICKS							# 70
	descend_end: int = 1

	write_versioned_function("zombies/mystery_box/move_anim_tick", f"""
scoreboard players remove #mb_move_timer {ns}.data 1

# Bear phase: start ascend interpolation on chest + bear
execute if score #mb_move_timer {ns}.data matches {ascend_start} run function {ns}:v{version}/zombies/mystery_box/move_anim_start_ascend

# Ascend phase: move chest + bear upward (slow then fast)
execute if score #mb_move_timer {ns}.data matches {ascend_end}..{ascend_start} run function {ns}:v{version}/zombies/mystery_box/move_anim_ascend_step

# End of ascend: kill old displays
execute if score #mb_move_timer {ns}.data matches {ascend_end - 1} run kill @e[tag={ns}.mb_display]
execute if score #mb_move_timer {ns}.data matches {ascend_end - 1} run kill @e[tag={ns}.mb_presence]

# Wait phase ({ascend_end - 1}..{transition + 1}): 5 seconds, no box visible

# Transition: pick new location, spawn descending chest
execute if score #mb_move_timer {ns}.data matches {transition} run function {ns}:v{version}/zombies/mystery_box/move_anim_transition

# Descend phase: chest descends at new location (fast then slow)
execute if score #mb_move_timer {ns}.data matches {descend_end}..{transition - 1} run function {ns}:v{version}/zombies/mystery_box/move_anim_descend_step

# Land: finalize
execute if score #mb_move_timer {ns}.data matches 0 run function {ns}:v{version}/zombies/mystery_box/move_anim_land
""")

	write_versioned_function("zombies/mystery_box/move_anim_start_ascend", f"""
# Enable smooth movement on chest and bear displays
data merge entity @n[tag={ns}.mb_presence] {{teleport_duration:5}}
data merge entity @n[tag={ns}.mb_display] {{teleport_duration:5}}
execute as @n[tag={ns}.mystery_box_active] at @s run function {ns}:v{version}/zombies/feedback/sound_box_disappear
""")

	# Ascend: slow first half, fast second half
	ascend_mid: int = ascend_end + MOVE_ASCEND_TICKS // 2	# 111
	write_versioned_function("zombies/mystery_box/move_anim_ascend_step", f"""
# Slow phase (first half): rise ~0.06 blocks/tick
execute if score #mb_move_timer {ns}.data matches {ascend_mid}..{ascend_start} as @n[tag={ns}.mb_presence] at @s run tp @s ~ ~0.06 ~
execute if score #mb_move_timer {ns}.data matches {ascend_mid}..{ascend_start} as @n[tag={ns}.mb_display] at @s run tp @s ~ ~0.06 ~

# Fast phase (second half): rise ~0.18 blocks/tick
execute if score #mb_move_timer {ns}.data matches {ascend_end}..{ascend_mid - 1} as @n[tag={ns}.mb_presence] at @s run tp @s ~ ~0.18 ~
execute if score #mb_move_timer {ns}.data matches {ascend_end}..{ascend_mid - 1} as @n[tag={ns}.mb_display] at @s run tp @s ~ ~0.18 ~

# Smoke particles at old location
execute at @n[tag={ns}.mystery_box_active] run particle minecraft:large_smoke ~ ~1 ~ 0.3 0.5 0.3 0.02 2 force
""")

	write_versioned_function("zombies/mystery_box/move_anim_transition", f"""
# Pick new active position
function {ns}:v{version}/zombies/mystery_box/move_active_position

# Spawn new chest display above the new active position (height = 0.7 + descent total)
# Fast: 35t * 0.18 = 6.3 blocks, Slow: 34t * 0.06 = 2.04 blocks, Total = 8.34
execute as @n[tag={ns}.mystery_box_active] at @s positioned ~ ~9.04 ~ run summon minecraft:item_display ~ ~ ~ {{Tags:["{ns}.mb_presence","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:chest",count:1}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.85f,0.85f,0.85f]}},teleport_duration:5}}
execute as @n[tag={ns}.mystery_box_active] at @s as @n[tag={ns}.mb_presence] run data modify entity @s Rotation set from entity @n[tag={ns}.mystery_box_active] Rotation

# Light beam particles at new location
execute at @n[tag={ns}.mystery_box_active] run particle minecraft:end_rod ~ ~3 ~ 0.1 2 0.1 0.05 20 force
execute as @n[tag={ns}.mystery_box_active] at @s run function {ns}:v{version}/zombies/feedback/sound_box_poof
""")

	# Descend: fast first half, slow second half (landing)
	descend_mid: int = MOVE_DESCEND_TICKS // 2		# 35
	write_versioned_function("zombies/mystery_box/move_anim_descend_step", f"""
# Fast phase (first half): descend ~0.18 blocks/tick
execute if score #mb_move_timer {ns}.data matches {descend_mid}..{transition - 1} as @n[tag={ns}.mb_presence] at @s run tp @s ~ ~-0.18 ~

# Slow phase (second half, landing): descend ~0.06 blocks/tick
execute if score #mb_move_timer {ns}.data matches {descend_end}..{descend_mid - 1} as @n[tag={ns}.mb_presence] at @s run tp @s ~ ~-0.06 ~

# Trailing particles
execute at @n[tag={ns}.mb_presence] run particle minecraft:end_rod ~ ~-0.5 ~ 0.2 0.1 0.2 0.01 1 force
""")

	write_versioned_function("zombies/mystery_box/move_anim_land", f"""
# Snap the descending chest to exact final position smoothly
execute as @n[tag={ns}.mystery_box_active] at @s as @n[tag={ns}.mb_presence] run tp @s ~ ~0.7 ~

# Reset move state
scoreboard players set #mb_move_timer {ns}.data 0
data remove storage {ns}:zombies mystery_box.result

# Announce arrival
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"The Mystery Box has arrived at a new location!","color":"yellow"}}]
execute as @n[tag={ns}.mystery_box_active] at @s run function {ns}:v{version}/zombies/feedback/sound_box_land
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
execute as @n[tag={ns}.mystery_box_active] at @s run function {ns}:v{version}/zombies/feedback/sound_box_close

# Remove buyer tag
tag @s remove {ns}.mb_buyer

# Reset box
function {ns}:v{version}/zombies/mystery_box/reset
""")

	write_versioned_function("zombies/mystery_box/capture_collected_name", f"""
$data modify storage {ns}:temp _mb_collected_name set value [{{"text":"$(weapon_id)","color":"gold"}}]
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
data modify storage smithed.actionbar:input message set value {json:[{"text":"🎲 Mystery Box","color":"light_purple"},{"text":" - ","color":"gray"},{"text":"Click to collect!","color":"green"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/mystery_box/hud_spinning", """
data modify storage smithed.actionbar:input message set value {json:[{"text":"🎲 Mystery Box","color":"light_purple"},{"text":" - ","color":"gray"},{"text":"Spinning...","color":"yellow"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/mystery_box/hud_price", """
data modify storage smithed.actionbar:input message set value {json:[{"text":"🎲 Mystery Box","color":"light_purple"},{"text":" - ","color":"gray"},{"text":"950 points","color":"gold"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/mystery_box/hud_moving", """
data modify storage smithed.actionbar:input message set value {json:[{"text":"🎲 Mystery Box","color":"light_purple"},{"text":" - ","color":"gray"},{"text":"Moving...","color":"yellow"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/mystery_box/on_hover", f"""
execute unless entity @e[tag=bs.interaction.target,tag={ns}.mystery_box_active] run return fail
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail
execute if score #mb_move_timer {ns}.data matches 1.. run return run function {ns}:v{version}/zombies/mystery_box/hud_moving
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
kill @e[tag={ns}.mb_presence]
scoreboard players set #mb_pulls {ns}.data 0
scoreboard players set #mb_move_timer {ns}.data 0
tag @a remove {ns}.mb_buyer
""")
