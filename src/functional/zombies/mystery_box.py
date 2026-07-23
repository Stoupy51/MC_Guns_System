
# ruff: noqa: E501
# Mystery Box System
# Dynamic weapon pool, visual animation with item cycling, random selection.
# Price: 950 points (configurable via #zb_mystery_box_price config)
# Pool can be extended via function tag #mgs:zombies/register_mystery_box_item
# Uses Bookshelf interaction module for click/hover detection.
# Positions use compound format: {pos:[x,y,z], rotation:[yaw,0.0f], group_id:N, can_start_on:1b}
from stewbeet import LootTable, Mem, set_json_encoder, write_load_file, write_versioned_function

from ...config.stats import WEIGHT
from ...database.weapons import WEAPON_STATS
from ..helpers import MGS_TAG
from .common import build_weapon_magazine_data

# Move animation constants
MOVE_BEAR_TICKS: int = 30		# bear visible before ascend starts
MOVE_ASCEND_TICKS: int = 80		# ascend at old location
MOVE_WAIT_TICKS: int = 100		# 5-second wait before descending
MOVE_DESCEND_TICKS: int = 70	# descend at new location
MOVE_TOTAL_TICKS: int = MOVE_BEAR_TICKS + MOVE_ASCEND_TICKS + MOVE_WAIT_TICKS + MOVE_DESCEND_TICKS	# 280

# Teddy bear player head texture (Black Ops easter egg)
BEAR_HEAD_TEXTURE: str = "eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvY2RiNjZjZjlmMTdlMTQ4OTMxMGM3YWNjNjgxMDE2MDUxMTk2YTg0OGUwNzZkYjZmYzA5MzkxYjkyODcyYTc3NyJ9fX0="

# Monkey Bomb pool weight (weapon weights come from the catalog; the monkey is a non-catalog
# tactical added to the pool manually — BO-style fairly common roll)
MONKEY_BOMB_WEIGHT: int = 5


def generate_mystery_box() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	owned_gun_macro_cd: str = "{" + ns + ':{gun:true,stats:{base_weapon:"$(weapon_id)"}}}'

	# Presence box is two item_displays (base + lid) sharing this scale, so the lid can hinge open.
	# 2.4 uniform scale makes the (full-width) model ~2.4 blocks wide.
	MB_SCALE: float = 2.4
	# Closed: identity. Open: hinge ~100° about X at the lid's front-bottom edge (like a real
	# chest lid opening toward the front). item_display rotates about the model centre, so the
	# translation cancels that out to keep the front-bottom edge fixed (T = p - R·p, with
	# p = scaled offset of the hinge from centre = (0, -0.15, -0.6) at scale 2.4; R = -100° about X).
	mb_closed_tf: str = f"{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[{MB_SCALE}f,{MB_SCALE}f,{MB_SCALE}f]}}"
	mb_open_tf: str = f"{{left_rotation:[-0.766f,0f,0f,0.643f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.415f,-0.652f],scale:[{MB_SCALE}f,{MB_SCALE}f,{MB_SCALE}f]}}"

	## Per-box state objectives (each box is an independent pull, so multiple can spin at once)
	write_load_file(f"""
# Box id shared by a box's interaction entity and its active pull display
scoreboard objectives add {ns}.mb.box dummy
# Spin animation timer carried by each pull display (>0 spinning, <=0 ready window)
scoreboard objectives add {ns}.mb.anim dummy
# 1 when the buyer of this pull owns Timeslip (spin runs 2x faster for their display)
scoreboard objectives add {ns}.mb.timeslip dummy
# Whether this pull will end in a box move (teddy bear) — only the active box, never Fire Sale
scoreboard objectives add {ns}.mb.willmove dummy
# Stable per-player id, assigned lazily on first pull, so a pull display can record WHICH player
# bought it. During a Fire Sale one player can have several pulls running at once, so the buyer
# must be tracked per-display (mb.buyer below) — a single "which box am I buying" value on the
# player would be overwritten by the second pull and orphan the first box's collectible.
scoreboard objectives add {ns}.mb.pid dummy
# Buyer's pid, stamped on each pull display
scoreboard objectives add {ns}.mb.buyer dummy
""")

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

	# Monkey Bomb: zombies-exclusive tactical (no magazine, given to hotbar.6 via the shared
	# wallbuys/give_tactical — holding any monkeys counts as "owned" so duplicates reroll)
	pool_entries.append(
		f'{{weapon_id:"monkey_bomb",'
		f'give_function:"{ns}:v{version}/zombies/mystery_box/default_give/monkey_bomb",'
		f'magazine_id:"",'
		f'mag_count:0,'
		f'consumable:0b}}'
	)
	pool_weights.append(MONKEY_BOMB_WEIGHT)
	default_pool_entries: str = ",".join(pool_entries)
	default_pool_weights: str = ",".join(str(w) for w in pool_weights)

	for weapon_id in default_pool_weapons:
		magazine_id, mag_count, is_consumable = weapon_mag_data[weapon_id]
		write_versioned_function(f"zombies/mystery_box/default_give/{weapon_id}", f"""
data modify storage {ns}:temp _wb_weapon set value {{weapon_id:"{weapon_id}",name:"{weapon_id}",consumable:{"1b" if is_consumable else "0b"},magazine_id:"{magazine_id}",mag_count:{mag_count}}}
scoreboard players set #wb_price {ns}.data 0
function {ns}:v{version}/zombies/wallbuys/process_purchase with storage {ns}:temp _wb_weapon
""")

	## Monkey Bomb give: routes to the tactical slot (hotbar.6) instead of the gun flow
	write_versioned_function("zombies/mystery_box/default_give/monkey_bomb", f"""
scoreboard players set #wb_price {ns}.data 0
function {ns}:v{version}/zombies/wallbuys/give_tactical {{weapon_id:"monkey_bomb"}}
""")

	write_versioned_function("zombies/mystery_box/ensure_default_pool", f"""
data modify storage {ns}:zombies mystery_box_pool set value [{default_pool_entries}]
data modify storage {ns}:zombies mystery_box_weights set value [{default_pool_weights}]
""")

	## Setup: iterate mystery box position compounds, summon interaction entities with Bookshelf
	write_versioned_function("zombies/mystery_box/setup_positions", f"""
# Summon mystery box markers at map positions
scoreboard players set #mb_box_counter {ns}.data 0
data modify storage {ns}:temp _mb_iter set from storage {ns}:zombies game.map.mystery_box.positions
execute if data storage {ns}:temp _mb_iter[0] run function {ns}:v{version}/zombies/mystery_box/setup_pos_iter

# Pick a random position with can_start_on as the active mystery box
execute as @n[tag={ns}.mystery_box_pos,tag={ns}.mb_can_start,sort=random] run tag @s add {ns}.mystery_box_active
# Fallback if no can_start_on positions exist
execute unless entity @e[tag={ns}.mystery_box_active] as @n[tag={ns}.mystery_box_pos,sort=random] run tag @s add {ns}.mystery_box_active

# Init pull counter and box-id counter, then spawn presence chest at the active position.
scoreboard players set #mb_pulls {ns}.data 0
scoreboard players set #mb_box_counter {ns}.data 0
function {ns}:v{version}/zombies/mystery_box/sync_presence_display

# Tuck away the interaction entities of every non-active box
function {ns}:v{version}/zombies/mystery_box/sync_interaction_visibility
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
execute as @n[tag={ns}.mb_new] at @s run tp @s ^ ^2 ^0.3

# Assign this box a unique id (shared later by its pull display)
scoreboard players add #mb_box_counter {ns}.data 1
scoreboard players operation @n[tag={ns}.mb_new] {ns}.mb.box = #mb_box_counter {ns}.data

# Tag entities that can_start_on
data modify storage {ns}:temp can_start_on set from storage {ns}:temp _mb_iter[0].can_start_on
execute if data storage {ns}:temp {{can_start_on:1b}} run tag @n[tag={ns}.mb_new] add {ns}.mb_can_start

# Register Bookshelf events on newly spawned entity
execute as @n[tag={ns}.mb_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/zombies/mystery_box/on_right_click",executor:"source"}}
execute as @n[tag={ns}.mb_new] run function #bs.interaction:on_hover {{run:"function {ns}:v{version}/zombies/mystery_box/on_hover",executor:"source"}}
execute as @n[tag={ns}.mb_new] run function #bs.interaction:on_left_click {{run:"function {ns}:v{version}/zombies/mystery_box/on_left_click",executor:"source"}}
tag @n[tag={ns}.mb_new] remove {ns}.mb_new

data remove storage {ns}:temp _mb_iter[0]
execute if data storage {ns}:temp _mb_iter[0] run function {ns}:v{version}/zombies/mystery_box/setup_pos_iter
""")

	write_versioned_function("zombies/mystery_box/summon_pos_at", f"""
$summon minecraft:interaction $(x) $(y) $(z) {{width:2.0f,height:-2.0f,response:true,Rotation:$(rotation),Tags:["{ns}.mystery_box_pos","{ns}.gm_entity","{ns}.mb_new","bs.entity.interaction"]}}
""")

	## Move each box's interaction entity out of reach unless its box is usable, so players can't
	## hover or right-click a dead box position (an unreachable interaction entity also can't eat a
	## gun click there). A box is usable when it's the active box, any box during a Fire Sale, or a
	## box with a pull still in progress (so the buyer can always collect). Each entity is offset by
	## exactly ±512 blocks so its real position stays exact across box moves. Called on every state
	## change (setup, box move, Fire Sale start/end/cleanup, pull collect/reset) — never per tick.
	write_versioned_function("zombies/mystery_box/sync_interaction_visibility", f"""
execute as @e[tag={ns}.mystery_box_pos] at @s run function {ns}:v{version}/zombies/mystery_box/sync_interaction_one
""")

	write_versioned_function("zombies/mystery_box/sync_interaction_one", f"""
# @s = a box interaction entity, at @s. Decide if it should be reachable.
scoreboard players set #mb_vis {ns}.data 0
execute if entity @s[tag={ns}.mystery_box_active] run scoreboard players set #mb_vis {ns}.data 1
execute if score #zb_fire_sale_timer {ns}.data matches 1.. if entity @s[tag={ns}.mb_fs_active] run scoreboard players set #mb_vis {ns}.data 1
execute if entity @n[tag={ns}.mb_display,distance=..3] run scoreboard players set #mb_vis {ns}.data 1

execute if score #mb_vis {ns}.data matches 1 if entity @s[tag={ns}.mb_hidden] run function {ns}:v{version}/zombies/mystery_box/interaction_show
execute if score #mb_vis {ns}.data matches 0 unless entity @s[tag={ns}.mb_hidden] run function {ns}:v{version}/zombies/mystery_box/interaction_hide
""")

	write_versioned_function("zombies/mystery_box/interaction_show", f"""
tp @s ~ ~512 ~
tag @s remove {ns}.mb_hidden
""")

	write_versioned_function("zombies/mystery_box/interaction_hide", f"""
tp @s ~ ~-512 ~
tag @s add {ns}.mb_hidden
""")

	write_versioned_function("zombies/mystery_box/sync_presence_display", f"""
# Keep one chest display at the currently active mystery box.
kill @e[tag={ns}.mb_presence]
execute as @n[tag={ns}.mystery_box_active] at @s run data modify storage {ns}:temp _mb_chest.yaw set value 0.0f
execute as @n[tag={ns}.mystery_box_active] at @s run data modify storage {ns}:temp _mb_chest.yaw set from entity @s Rotation[0]
execute as @n[tag={ns}.mystery_box_active] at @s run function {ns}:v{version}/zombies/mystery_box/summon_presence_display with storage {ns}:temp _mb_chest
""")

	write_versioned_function("zombies/mystery_box/summon_presence_display", f"""
# Two-piece presence box: base + lid (both tagged mb_presence so they move/despawn together).
$execute positioned ~ ~-0.9 ~ run summon minecraft:item_display ~ ~ ~ {{Rotation:[$(yaw),0f],Tags:["{ns}.mb_presence","{ns}.mb_base","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:chest",count:1,components:{{"minecraft:item_model":"{ns}:mystery_box_base"}}}},transformation:{mb_closed_tf}}}
$execute positioned ~ ~-0.9 ~ run summon minecraft:item_display ~ ~ ~ {{Rotation:[$(yaw),0f],Tags:["{ns}.mb_presence","{ns}.mb_lid","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:chest",count:1,components:{{"minecraft:item_model":"{ns}:mystery_box_lid"}}}},transformation:{mb_closed_tf}}}
""")

	## Lid open/close animation (interpolated). Position-based: affects only the lid nearest the
	## current execution position, so callers must be positioned at the box they mean.
	write_versioned_function("zombies/mystery_box/open_lid", f"""
data merge entity @n[tag={ns}.mb_lid,distance=..4] {{transformation:{mb_open_tf},start_interpolation:0,interpolation_duration:8}}
""")
	write_versioned_function("zombies/mystery_box/close_lid", f"""
data merge entity @n[tag={ns}.mb_lid,distance=..4] {{transformation:{mb_closed_tf},start_interpolation:0,interpolation_duration:8}}
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

	## On right-click: Bookshelf callback (executor:"source" = @s is the player).
	## Each box is an independent pull, so dispatch based on the clicked box's own state.
	write_versioned_function("zombies/mystery_box/on_right_click", f"""
# A box is usable if it's the active box, any box during a Fire Sale, or a box that still has a
# pull in progress (so a buyer can always collect/finish a pull even after a Fire Sale ended).
scoreboard players set #mb_usable {ns}.data 0
execute if entity @e[tag=bs.interaction.target,tag={ns}.mystery_box_active] run scoreboard players set #mb_usable {ns}.data 1
execute if score #zb_fire_sale_timer {ns}.data matches 1.. if entity @e[tag=bs.interaction.target,tag={ns}.mb_fs_active] run scoreboard players set #mb_usable {ns}.data 1
execute at @n[tag=bs.interaction.target] if entity @n[tag={ns}.mb_display,distance=..3] run scoreboard players set #mb_usable {ns}.data 1
execute if score #mb_usable {ns}.data matches 0 run return fail

# Check game is active
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail

# The active box can be mid-move: deny
execute if score #mb_move_timer {ns}.data matches 1.. if entity @e[tag=bs.interaction.target,tag={ns}.mystery_box_active] run return run function {ns}:v{version}/zombies/mystery_box/deny_moving

# Capture the clicked box id, then dispatch at the box position
scoreboard players operation #cur_box {ns}.data = @n[tag=bs.interaction.target] {ns}.mb.box
execute at @n[tag=bs.interaction.target] run function {ns}:v{version}/zombies/mystery_box/box_click
""")

	## Shift + left click: hand your finished pull to the team (@s = player)
	write_versioned_function("zombies/mystery_box/on_left_click", f"""
# Plain left click is a normal swing, only sneaking means "share this"
execute unless predicate {ns}:v{version}/is_sneaking run return fail
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail
execute at @n[tag=bs.interaction.target] run function {ns}:v{version}/zombies/mystery_box/share_at_box
""")

	## Mark this box's finished pull as free for anyone to collect (@s = player, at the box)
	write_versioned_function("zombies/mystery_box/share_at_box", f"""
# Nothing to share unless a finished pull is sitting here (a spinning one has no weapon yet)
execute unless entity @n[tag={ns}.mb_display,distance=..3] run return fail
execute if entity @n[tag={ns}.mb_display,distance=..3,scores={{{ns}.mb.anim=1..}}] run return fail

# Sharing twice is a no-op rather than a second announcement
execute if entity @n[tag={ns}.mb_display,distance=..3,tag={ns}.mb_shared] run return fail

# Only the buyer can give their own pull away
execute unless score @s {ns}.mb.pid = @n[tag={ns}.mb_display,distance=..3] {ns}.mb.buyer run return run function {ns}:v{version}/zombies/mystery_box/deny_not_your_result

tag @n[tag={ns}.mb_display,distance=..3] add {ns}.mb_shared
function {ns}:v{version}/zombies/feedback/sound_success
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"selector":"@s"}},{{"text":" shared their Mystery Box weapon — anyone can take it!","color":"green"}}]
""")

	## Dispatch a click at a specific box (@s = player, positioned at the box)
	write_versioned_function("zombies/mystery_box/box_click", f"""
# Spinning (a pull display here with anim > 0): already in use
execute if entity @n[tag={ns}.mb_display,distance=..3,scores={{{ns}.mb.anim=1..}}] run return run function {ns}:v{version}/zombies/mystery_box/deny_already_in_use

# Shared by its buyer (shift + left click): anyone may collect it
execute if entity @n[tag={ns}.mb_display,distance=..3,tag={ns}.mb_shared] run return run function {ns}:v{version}/zombies/mystery_box/collect

# Ready (a display here, anim <= 0): only the buyer of this box may collect (buyer pid matches)
execute if entity @n[tag={ns}.mb_display,distance=..3] if score @s {ns}.mb.pid = @n[tag={ns}.mb_display,distance=..3] {ns}.mb.buyer run return run function {ns}:v{version}/zombies/mystery_box/collect
execute if entity @n[tag={ns}.mb_display,distance=..3] run return run function {ns}:v{version}/zombies/mystery_box/deny_not_your_result

# No pull on this box yet: start one
function {ns}:v{version}/zombies/mystery_box/try_use
""")

	# Begin a Fire Sale: remember the original box, flag all positions usable, spawn temp boxes.
	write_versioned_function("zombies/mystery_box/fire_sale_start", f"""
tag @e[tag={ns}.mystery_box_active] add {ns}.mb_orig_active
tag @e[tag={ns}.mystery_box_pos] add {ns}.mb_fs_active

# Every box is usable now: bring all interaction entities back into reach. This MUST happen before
# the temp boxes are summoned below — a hidden interaction entity is parked 512 blocks under its
# real position (see interaction_hide), and the chest models are summoned `at @s`, so summoning
# first buried every fire-sale chest underground: the box was usable but its model was invisible.
function {ns}:v{version}/zombies/mystery_box/sync_interaction_visibility

execute as @e[tag={ns}.mystery_box_pos,tag=!{ns}.mystery_box_active] at @s run function {ns}:v{version}/zombies/mystery_box/fire_sale_summon_box
""")

	write_versioned_function("zombies/mystery_box/fire_sale_summon_box", f"""
data modify storage {ns}:temp _mb_fs.yaw set value 0.0f
data modify storage {ns}:temp _mb_fs.yaw set from entity @s Rotation[0]
function {ns}:v{version}/zombies/mystery_box/summon_temp_box with storage {ns}:temp _mb_fs
""")

	write_versioned_function("zombies/mystery_box/summon_temp_box", f"""
$execute positioned ~ ~-0.9 ~ run summon minecraft:item_display ~ ~ ~ {{Rotation:[$(yaw),0f],Tags:["{ns}.mb_presence","{ns}.mb_base","{ns}.mb_temp","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:chest",count:1,components:{{"minecraft:item_model":"{ns}:mystery_box_base"}}}},transformation:{mb_closed_tf}}}
$execute positioned ~ ~-0.9 ~ run summon minecraft:item_display ~ ~ ~ {{Rotation:[$(yaw),0f],Tags:["{ns}.mb_presence","{ns}.mb_lid","{ns}.mb_temp","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:chest",count:1,components:{{"minecraft:item_model":"{ns}:mystery_box_lid"}}}},transformation:{mb_closed_tf}}}
""")

	# End a Fire Sale: stop allowing temp pulls; clean up now if idle, else defer until the
	# in-progress pull resets (so a box being used isn't yanked mid-spin).
	write_versioned_function("zombies/mystery_box/fire_sale_end", f"""
tag @e[tag={ns}.mb_fs_active] remove {ns}.mb_fs_active
# Re-hide interaction entities of boxes that are no longer usable (boxes with a pull still in
# progress stay reachable via the sync's pull-in-progress check, so buyers can still collect).
function {ns}:v{version}/zombies/mystery_box/sync_interaction_visibility
# If any pull is in progress, defer cleanup until the last display resets; otherwise clean up now.
execute if entity @e[tag={ns}.mb_display] run return run scoreboard players set #mb_fs_cleanup_pending {ns}.data 1
function {ns}:v{version}/zombies/mystery_box/fire_sale_cleanup
""")

	write_versioned_function("zombies/mystery_box/fire_sale_cleanup", f"""
# Remove every temporary box and clear Fire-Sale bookkeeping. The active box never changes during
# a Fire Sale, so we must NOT touch the mystery_box_active tag here (doing so could strip it off
# every box if state is inconsistent, leaving no usable box).
tag @e[tag={ns}.mb_orig_active] remove {ns}.mb_orig_active
kill @e[tag={ns}.mb_temp]
scoreboard players set #mb_fs_cleanup_pending {ns}.data 0

# Non-active boxes are dead again: tuck their interaction entities away
function {ns}:v{version}/zombies/mystery_box/sync_interaction_visibility
""")

	write_versioned_function("zombies/mystery_box/deny_moving", f"""
tellraw @s [{MGS_TAG},{{"text":"The Mystery Box is moving...","color":"yellow"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

	write_versioned_function("zombies/mystery_box/deny_already_in_use", f"""
tellraw @s [{MGS_TAG},{{"text":"Mystery Box is already in use.","color":"red"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

	## Start a pull on the clicked box (@s = player, positioned at the box, #cur_box = box id)
	write_versioned_function("zombies/mystery_box/try_use", f"""
# Check if player has enough points
execute unless score @s {ns}.zb.points >= #zb_mystery_box_price {ns}.config run return run function {ns}:v{version}/zombies/mystery_box/deny_not_enough_points

# Ensure at least a default pool exists.
function {ns}:v{version}/zombies/mystery_box/ensure_default_pool

# Deduct points, then ensure this player has a stable id so the pull display can record them as
# its buyer (set on the display below). Supports several concurrent pulls by the same player.
scoreboard players operation @s {ns}.zb.points -= #zb_mystery_box_price {ns}.config
execute unless score @s {ns}.mb.pid matches 1.. run function {ns}:v{version}/zombies/mystery_box/assign_pid

# Pre-determine if the box will move (teddy bear) — only the active box, never during a Fire Sale
scoreboard players set #mb_will_move {ns}.data 0
scoreboard players add #mb_pulls {ns}.data 1
execute if score #mb_pulls {ns}.data matches 4.. if entity @n[tag=bs.interaction.target,tag={ns}.mystery_box_active] store result score #mb_move_roll {ns}.data run random value 0..2
execute if score #mb_pulls {ns}.data matches 4.. if entity @n[tag=bs.interaction.target,tag={ns}.mystery_box_active] if score #mb_move_roll {ns}.data matches 0 run scoreboard players set #mb_will_move {ns}.data 1
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
function {ns}:v{version}/zombies/feedback/sound_box_open
# Timeslip owners get the sped-up spin tune to match their 2x pull
execute unless score @s {ns}.special.timeslip matches 1.. run function {ns}:v{version}/zombies/feedback/sound_box_spin
execute if score @s {ns}.special.timeslip matches 1.. run function {ns}:v{version}/zombies/feedback/sound_box_spin_short
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
$execute if items entity @s hotbar.1 *[custom_data~{owned_gun_macro_cd}] run scoreboard players set #mb_owned {ns}.data 1
$execute if items entity @s hotbar.2 *[custom_data~{owned_gun_macro_cd}] run scoreboard players set #mb_owned {ns}.data 1
$execute if items entity @s hotbar.3 *[custom_data~{owned_gun_macro_cd}] run scoreboard players set #mb_owned {ns}.data 1
# Tactical slot (monkey bombs): holding any counts as owned, so the box rerolls like duplicate guns
$execute if items entity @s hotbar.6 *[custom_data~{owned_gun_macro_cd}] run scoreboard players set #mb_owned {ns}.data 1

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

	write_versioned_function("zombies/mystery_box/deny_pool_empty", f"""
# Clear any stale result so downstream checks treat this pull as failed
data remove storage {ns}:zombies mystery_box.result
tellraw @s [{MGS_TAG},{{"text":"The Mystery Box has no weapons available.","color":"red"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""")

	## Display entity: spawned at box level; floats up via the per-display tick (anim==104).
	write_versioned_function("zombies/mystery_box/spawn_display", f"""
summon minecraft:item_display ~ ~-1.5 ~ {{Tags:["{ns}.mb_display","{ns}.gm_entity","{ns}.mb_display_new"],item_display:"fixed",item:{{id:"minecraft:nether_star",count:1,components:{{"minecraft:item_model":"air"}}}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.4f,0.4f,0.4f]}},billboard:"fixed"}}
tp @n[tag={ns}.mb_display_new] ~ ~-1.5 ~ ~ ~
""")

	## Mystery box tick: each pull display advances independently, so multiple boxes can spin at once.
	write_versioned_function("zombies/mystery_box/tick", f"""
# Per-box spin animation (the moving bear display is excluded — the move handles it)
execute as @e[tag={ns}.mb_display,tag=!{ns}.mb_bear] at @s run function {ns}:v{version}/zombies/mystery_box/spin_tick_one

# Move animation tick (active box only; never during a Fire Sale)
execute if score #mb_move_timer {ns}.data matches 1.. run function {ns}:v{version}/zombies/mystery_box/move_anim_tick
""")

	## Per-display spin tick (@s = a pull display, never the moving bear)
	write_versioned_function("zombies/mystery_box/spin_tick_one", f"""
scoreboard players remove @s {ns}.mb.anim 1

# Timeslip: 2x spin speed. The extra -1 only fires inside the cycling phase (1..103), so the 104
# float-up trigger still runs; anim is even every tick after the first, so the doubled step always
# lands exactly on the anim==0 result and never overshoots into the reset window.
execute if score @s {ns}.mb.timeslip matches 1 if score @s {ns}.mb.anim matches 1..103 run scoreboard players remove @s {ns}.mb.anim 1

# Start the float-up one tick after spawn (avoids same-tick interpolation glitches)
execute if score @s {ns}.mb.anim matches 104 run data merge entity @s {{transformation:{{translation:[0f,0.8f,0f]}},start_interpolation:0,interpolation_duration:200}}

# Cycling phase (anim > 0): show random items with staged slowdown cadence
execute if score @s {ns}.mb.anim matches 1.. run function {ns}:v{version}/zombies/mystery_box/cycle_step_one

# Landing (anim == 0): decide + show the result
execute if score @s {ns}.mb.anim matches 0 run function {ns}:v{version}/zombies/mystery_box/show_result_one

# Pickup window expired (anim == -150): remove display and reset this box
execute if score @s {ns}.mb.anim matches ..-150 run function {ns}:v{version}/zombies/mystery_box/reset_one
""")

	## Cadence using the display's own anim timer (@s = display)
	write_versioned_function("zombies/mystery_box/cycle_step_one", f"""
scoreboard players set #mb_elapsed {ns}.data 80
scoreboard players operation #mb_elapsed {ns}.data -= @s {ns}.mb.anim
scoreboard players set #mb_c2 {ns}.data 2
scoreboard players set #mb_c5 {ns}.data 5
scoreboard players set #mb_c8 {ns}.data 8

scoreboard players operation #mb_mod {ns}.data = #mb_elapsed {ns}.data
execute if score #mb_elapsed {ns}.data matches ..29 run scoreboard players operation #mb_mod {ns}.data %= #mb_c2 {ns}.data
execute if score #mb_elapsed {ns}.data matches ..29 if score #mb_mod {ns}.data matches 0 run function {ns}:v{version}/zombies/mystery_box/cycle_display_one

scoreboard players operation #mb_mod {ns}.data = #mb_elapsed {ns}.data
execute if score #mb_elapsed {ns}.data matches 30..49 run scoreboard players operation #mb_mod {ns}.data %= #mb_c5 {ns}.data
execute if score #mb_elapsed {ns}.data matches 30..49 if score #mb_mod {ns}.data matches 0 run function {ns}:v{version}/zombies/mystery_box/cycle_display_one

scoreboard players operation #mb_mod {ns}.data = #mb_elapsed {ns}.data
execute if score #mb_elapsed {ns}.data matches 50.. run scoreboard players operation #mb_mod {ns}.data %= #mb_c8 {ns}.data
execute if score #mb_elapsed {ns}.data matches 50.. if score #mb_mod {ns}.data matches 0 run function {ns}:v{version}/zombies/mystery_box/cycle_display_one
""")

	## Cycle this display's item (@s = display)
	write_versioned_function("zombies/mystery_box/cycle_display_one", f"""
data modify storage bs:in random.weighted_choice.options set from storage {ns}:zombies mystery_box_pool
data modify storage bs:in random.weighted_choice.weights set from storage {ns}:zombies mystery_box_weights
function #bs.random:weighted_choice
data modify storage {ns}:temp _mb_cycle_item set from storage bs:out random.weighted_choice
execute if data storage {ns}:temp _mb_cycle_item.weapon_id run function {ns}:v{version}/zombies/mystery_box/cycle_display_weapon_one with storage {ns}:temp _mb_cycle_item
execute unless data storage {ns}:temp _mb_cycle_item.weapon_id run data modify entity @s item set from storage {ns}:temp _mb_cycle_item.display_item
""")

	write_versioned_function("zombies/mystery_box/cycle_display_weapon_one", f"""
$loot replace entity @s contents loot {ns}:i/$(weapon_id)
""")


	## Landing: decide + show the result for this pull (@s = display, positioned at the box)
	write_versioned_function("zombies/mystery_box/show_result_one", f"""
# Box will move (active box only): teddy bear path
execute if score @s {ns}.mb.willmove matches 1 run return run function {ns}:v{version}/zombies/mystery_box/show_bear_result

# Remember this box's id and buyer, then pick + reroll the result as its buyer
scoreboard players operation #this_box {ns}.data = @s {ns}.mb.box
scoreboard players operation #this_buyer {ns}.data = @s {ns}.mb.buyer
data remove storage {ns}:zombies mystery_box.result
scoreboard players set #mb_owned {ns}.data 0
execute as @a[scores={{{ns}.zb.in_game=1}}] if score @s {ns}.mb.pid = #this_buyer {ns}.data run function {ns}:v{version}/zombies/mystery_box/pick_for_buyer

# All owned / empty pool: refund the buyer and cancel this pull
execute if score #mb_owned {ns}.data matches 1 run function {ns}:v{version}/zombies/mystery_box/result_all_owned
execute if score #mb_owned {ns}.data matches 1 run return run function {ns}:v{version}/zombies/mystery_box/reset_one

# Set this display to the final weapon and bake the result onto it for collect
execute if data storage {ns}:zombies mystery_box.result.weapon_id run function {ns}:v{version}/zombies/mystery_box/show_result_weapon_one with storage {ns}:zombies mystery_box.result
execute unless data storage {ns}:zombies mystery_box.result.weapon_id run data modify entity @s item set from storage {ns}:zombies mystery_box.result.display_item
data modify entity @s item.components."minecraft:custom_data".{ns}.mb_result set from storage {ns}:zombies mystery_box.result

# Descend into place over 7.5s (150 ticks)
data merge entity @s {{transformation:{{translation:[0f,1.5f,0f]}}}}
data merge entity @s {{interpolation_duration:150,transformation:{{translation:[0f,0f,0f]}},start_interpolation:0}}

# Tell only the buyer it is ready
execute as @a[scores={{{ns}.zb.in_game=1}}] if score @s {ns}.mb.pid = #this_buyer {ns}.data run tellraw @s [{MGS_TAG},{{"text":"Mystery Box result ready! ","color":"light_purple"}},{{"text":"Right-click to collect!","color":"green","bold":true}}]
""")

	## Pick + reroll the result against the buyer's owned weapons (@s = the buyer)
	write_versioned_function("zombies/mystery_box/pick_for_buyer", f"""
function {ns}:v{version}/zombies/mystery_box/pick_random_result
scoreboard players set #mb_reroll {ns}.data 0
function {ns}:v{version}/zombies/mystery_box/reroll_owned
# Treat a missing result (empty pool / all owned after rerolls) as "owned" so we refund
execute unless data storage {ns}:zombies mystery_box.result.weapon_id run scoreboard players set #mb_owned {ns}.data 1
""")

	## Refund the buyer of this box (#this_buyer set by show_result_one) and notify them
	write_versioned_function("zombies/mystery_box/result_all_owned", f"""
execute as @a[scores={{{ns}.zb.in_game=1}}] if score @s {ns}.mb.pid = #this_buyer {ns}.data run scoreboard players operation @s {ns}.zb.points += #zb_mystery_box_price {ns}.config
execute as @a[scores={{{ns}.zb.in_game=1}}] if score @s {ns}.mb.pid = #this_buyer {ns}.data run function {ns}:v{version}/zombies/mystery_box/deny_all_owned
""")

	write_versioned_function("zombies/mystery_box/show_result_weapon_one", f"""
$loot replace entity @s contents loot {ns}:i/$(weapon_id)
""")

	## Teddy bear result: box is about to move (Black Ops style). @s = the active box's display.
	write_versioned_function("zombies/mystery_box/show_bear_result", f"""
# Close this box's lid before it moves away
function {ns}:v{version}/zombies/mystery_box/close_lid

# Mark this display as the moving bear so the move animation only touches it (not other pulls)
tag @s add {ns}.mb_bear

# Replace display with teddy bear
loot replace entity @s contents loot {ns}:zombies/mystery_box_bear
data merge entity @s {{transformation:{{translation:[0f,1.25f,0f],scale:[0.75f,0.75f,0.75f]}}}}

# Refund this box's buyer (the moving box eats the pull, no weapon given)
scoreboard players operation #this_buyer {ns}.data = @s {ns}.mb.buyer
execute as @a[scores={{{ns}.zb.in_game=1}}] if score @s {ns}.mb.pid = #this_buyer {ns}.data run scoreboard players operation @s {ns}.zb.points += #zb_mystery_box_price {ns}.config

# Start move animation timer (this display is killed by the move at the ascend phase)
scoreboard players set #mb_move_timer {ns}.data {MOVE_TOTAL_TICKS}

tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"The Mystery Box is moving!","color":"yellow","bold":true}}]
function {ns}:v{version}/zombies/feedback/sound_box_bye_bye
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

# End of ascend: kill the moving bear + the old (non-temp) presence box only
execute if score #mb_move_timer {ns}.data matches {ascend_end - 1} run kill @e[tag={ns}.mb_bear]
execute if score #mb_move_timer {ns}.data matches {ascend_end - 1} run kill @e[tag={ns}.mb_presence,tag=!{ns}.mb_temp]
# If a Fire Sale had ended and that bear was the last in-progress display, finish temp cleanup now
execute if score #mb_move_timer {ns}.data matches {ascend_end - 1} if score #mb_fs_cleanup_pending {ns}.data matches 1 unless entity @e[tag={ns}.mb_display] run function {ns}:v{version}/zombies/mystery_box/fire_sale_cleanup

# Wait phase ({ascend_end - 1}..{transition + 1}): 5 seconds, no box visible

# Transition: pick new location, spawn descending chest
execute if score #mb_move_timer {ns}.data matches {transition} run function {ns}:v{version}/zombies/mystery_box/move_anim_transition

# Descend phase: chest descends at new location (fast then slow)
execute if score #mb_move_timer {ns}.data matches {descend_end}..{transition - 1} run function {ns}:v{version}/zombies/mystery_box/move_anim_descend_step

# Land: finalize
execute if score #mb_move_timer {ns}.data matches 0 run function {ns}:v{version}/zombies/mystery_box/move_anim_land
""")

	write_versioned_function("zombies/mystery_box/move_anim_start_ascend", f"""
# Enable smooth movement on the active chest (base + lid) and the bear display only
execute as @e[tag={ns}.mb_presence,tag=!{ns}.mb_temp] run data merge entity @s {{teleport_duration:5}}
execute as @e[tag={ns}.mb_bear] run data merge entity @s {{teleport_duration:5}}
execute as @n[tag={ns}.mystery_box_active] at @s run function {ns}:v{version}/zombies/feedback/sound_box_disappear
""")

	# Ascend: slow first half, fast second half
	ascend_mid: int = ascend_end + MOVE_ASCEND_TICKS // 2	# 111
	write_versioned_function("zombies/mystery_box/move_anim_ascend_step", f"""
# Slow phase (first half): rise ~0.06 blocks/tick
execute if score #mb_move_timer {ns}.data matches {ascend_mid}..{ascend_start} as @e[tag={ns}.mb_presence,tag=!{ns}.mb_temp] at @s run tp @s ~ ~0.06 ~
execute if score #mb_move_timer {ns}.data matches {ascend_mid}..{ascend_start} as @e[tag={ns}.mb_bear] at @s run tp @s ~ ~0.06 ~

# Fast phase (second half): rise ~0.18 blocks/tick
execute if score #mb_move_timer {ns}.data matches {ascend_end}..{ascend_mid - 1} as @e[tag={ns}.mb_presence,tag=!{ns}.mb_temp] at @s run tp @s ~ ~0.18 ~
execute if score #mb_move_timer {ns}.data matches {ascend_end}..{ascend_mid - 1} as @e[tag={ns}.mb_bear] at @s run tp @s ~ ~0.18 ~

# Smoke particles at old location
execute at @n[tag={ns}.mystery_box_active] run particle minecraft:large_smoke ~ ~1 ~ 0.3 0.5 0.3 0.02 2 force @a[distance=..48]
""")

	write_versioned_function("zombies/mystery_box/move_anim_transition", f"""
# Pick new active position
function {ns}:v{version}/zombies/mystery_box/move_active_position

# Bring the new active box's interaction entity into reach (and hide the old one) BEFORE the chest
# is positioned relative to it below — otherwise the chest would spawn at the hidden -512 offset.
function {ns}:v{version}/zombies/mystery_box/sync_interaction_visibility

# Spawn new chest display (base + lid) above the new active position (height = 0.7 + descent total)
# Fast: 35t * 0.18 = 6.3 blocks, Slow: 34t * 0.06 = 2.04 blocks, Total = 8.34
execute as @n[tag={ns}.mystery_box_active] at @s positioned ~ ~7.54 ~ run summon minecraft:item_display ~ ~ ~ {{Tags:["{ns}.mb_presence","{ns}.mb_base","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:chest",count:1,components:{{"minecraft:item_model":"{ns}:mystery_box_base"}}}},transformation:{mb_closed_tf},teleport_duration:5}}
execute as @n[tag={ns}.mystery_box_active] at @s positioned ~ ~7.54 ~ run summon minecraft:item_display ~ ~ ~ {{Tags:["{ns}.mb_presence","{ns}.mb_lid","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:chest",count:1,components:{{"minecraft:item_model":"{ns}:mystery_box_lid"}}}},transformation:{mb_closed_tf},teleport_duration:5}}
execute as @n[tag={ns}.mystery_box_active] at @s as @e[tag={ns}.mb_presence,tag=!{ns}.mb_temp] run data modify entity @s Rotation set from entity @n[tag={ns}.mystery_box_active] Rotation

# Light beam particles at new location
execute at @n[tag={ns}.mystery_box_active] run particle minecraft:end_rod ~ ~3 ~ 0.1 2 0.1 0.05 20 force @a[distance=..64]
execute as @n[tag={ns}.mystery_box_active] at @s run function {ns}:v{version}/zombies/feedback/sound_box_poof
""")

	# Descend: fast first half, slow second half (landing)
	descend_mid: int = MOVE_DESCEND_TICKS // 2		# 35
	write_versioned_function("zombies/mystery_box/move_anim_descend_step", f"""
# Fast phase (first half): descend ~0.18 blocks/tick
execute if score #mb_move_timer {ns}.data matches {descend_mid}..{transition - 1} as @e[tag={ns}.mb_presence,tag=!{ns}.mb_temp] at @s run tp @s ~ ~-0.18 ~

# Slow phase (second half, landing): descend ~0.06 blocks/tick
execute if score #mb_move_timer {ns}.data matches {descend_end}..{descend_mid - 1} as @e[tag={ns}.mb_presence,tag=!{ns}.mb_temp] at @s run tp @s ~ ~-0.06 ~

# Trailing particles
execute at @n[tag={ns}.mb_presence,tag=!{ns}.mb_temp] run particle minecraft:end_rod ~ ~-0.5 ~ 0.2 0.1 0.2 0.01 1 force @a[distance=..48]
""")

	write_versioned_function("zombies/mystery_box/move_anim_land", f"""
# Snap the descending chest (base + lid) to exact final position smoothly
execute as @n[tag={ns}.mystery_box_active] at @s as @e[tag={ns}.mb_presence,tag=!{ns}.mb_temp] run tp @s ~ ~-0.9 ~

# Reset move state
scoreboard players set #mb_move_timer {ns}.data 0
data remove storage {ns}:zombies mystery_box.result

# Announce arrival
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"The Mystery Box has arrived at a new location!","color":"yellow"}}]
execute as @n[tag={ns}.mystery_box_active] at @s run function {ns}:v{version}/zombies/feedback/sound_box_land
""")

	## Collect this box's result (called from box_click, @s = player, positioned at the box)
	write_versioned_function("zombies/mystery_box/collect", f"""
# Load the result baked onto this box's display
data modify storage {ns}:zombies mystery_box.result set from entity @n[tag={ns}.mb_display,distance=..3] item.components."minecraft:custom_data".{ns}.mb_result

# Give the result item to the player via its give function
scoreboard players set #wb_purchase_done {ns}.data 0
scoreboard players set #wb_purchase_mode {ns}.data -1
execute if data storage {ns}:zombies mystery_box.result.give_function run function {ns}:v{version}/zombies/mystery_box/give_via_function

# If the give flow failed (e.g. invalid selected slot), keep the result ready for retry.
execute if score #wb_purchase_done {ns}.data matches 0 run return 0

# Resolve the collected weapon display name from the given item.
execute if data storage {ns}:zombies mystery_box.result.weapon_id run function {ns}:v{version}/zombies/mystery_box/capture_collected_name with storage {ns}:zombies mystery_box.result

# Announce + sounds
tellraw @s [{MGS_TAG},{{"text":"You collected ","color":"green"}},{{"storage":"{ns}:temp","nbt":"_mb_collected_name","interpret":true}},{{"text":" from the Mystery Box.","color":"green"}}]
function {ns}:v{version}/zombies/feedback/sound_success
function {ns}:v{version}/zombies/feedback/sound_box_close

# Close this box's lid and remove its display (buyer is tracked per-display, nothing to clear)
function {ns}:v{version}/zombies/mystery_box/close_lid
kill @n[tag={ns}.mb_display,distance=..3]

# If a Fire Sale ended while pulls were in progress, finish temp-box cleanup once none remain
execute if score #mb_fs_cleanup_pending {ns}.data matches 1 unless entity @e[tag={ns}.mb_display] run function {ns}:v{version}/zombies/mystery_box/fire_sale_cleanup

# This box's pull is done: if it's no longer usable (e.g. a Fire-Sale box after the sale), hide it
function {ns}:v{version}/zombies/mystery_box/sync_interaction_visibility
""")

	write_versioned_function("zombies/mystery_box/capture_collected_name", f"""
$data modify storage {ns}:temp _mb_collected_name set value [{{"text":"$(weapon_id)","color":"gold"}}]
scoreboard players set #mb_name_found {ns}.data 0

$execute if score #mb_name_found {ns}.data matches 0 if items entity @s hotbar.1 *[custom_data~{owned_gun_macro_cd}] run function {ns}:v{version}/zombies/mystery_box/capture_collected_name_slot {{slot:"hotbar.1"}}
$execute if score #mb_name_found {ns}.data matches 0 if items entity @s hotbar.2 *[custom_data~{owned_gun_macro_cd}] run function {ns}:v{version}/zombies/mystery_box/capture_collected_name_slot {{slot:"hotbar.2"}}
$execute if score #mb_name_found {ns}.data matches 0 if items entity @s hotbar.3 *[custom_data~{owned_gun_macro_cd}] run function {ns}:v{version}/zombies/mystery_box/capture_collected_name_slot {{slot:"hotbar.3"}}
$execute if score #mb_name_found {ns}.data matches 0 if items entity @s hotbar.6 *[custom_data~{owned_gun_macro_cd}] run function {ns}:v{version}/zombies/mystery_box/capture_collected_name_slot {{slot:"hotbar.6"}}
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

	## Reset a single pull (@s = display, positioned at the box). Expires the display & closes its lid.
	write_versioned_function("zombies/mystery_box/reset_one", f"""
# Close this box's lid
function {ns}:v{version}/zombies/mystery_box/close_lid

# Remove the display (buyer is tracked per-display, nothing to clear on the player)
kill @s

# If a Fire Sale ended while pulls were in progress, finish temp-box cleanup once none remain
execute if score #mb_fs_cleanup_pending {ns}.data matches 1 unless entity @e[tag={ns}.mb_display] run function {ns}:v{version}/zombies/mystery_box/fire_sale_cleanup

# This box's pull ended: if it's no longer usable (e.g. a Fire-Sale box after the sale), hide it
function {ns}:v{version}/zombies/mystery_box/sync_interaction_visibility
""")

	## Hover functions for active mystery box
	write_versioned_function("zombies/mystery_box/hud_ready", """
data modify storage smithed.actionbar:input message set value {json:[{"text":"🎲 Mystery Box","color":"light_purple"},{"text":" - ","color":"gray"},{"text":"Click to collect!","color":"green"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message
""")

	# Ready + the weapon name is known: prompt the pick-up by name, e.g. "🎲 Pick-up Ray Gun"
	# (_mb_hover_name is the ready display item's item_name, read in hover_at_box)
	write_versioned_function("zombies/mystery_box/hud_ready_named", f"""
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"🎲 ","color":"light_purple"}},{{"text":"Pick-up ","color":"green"}},{{"storage":"{ns}:temp","nbt":"_mb_hover_name","interpret":true}}],priority:"conditional",freeze:5}}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/mystery_box/hud_spinning", """
data modify storage smithed.actionbar:input message set value {json:[{"text":"🎲 Mystery Box","color":"light_purple"},{"text":" - ","color":"gray"},{"text":"Spinning...","color":"yellow"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/mystery_box/hud_price", f"""
data modify storage smithed.actionbar:input message set value {{json:[{{"text":"🎲 Mystery Box","color":"light_purple"}},{{"text":" - ","color":"gray"}},{{"score":{{"name":"#zb_mystery_box_price","objective":"{ns}.config"}},"color":"gold"}},{{"text":" points","color":"gold"}}],priority:"conditional",freeze:5}}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/mystery_box/hud_moving", """
data modify storage smithed.actionbar:input message set value {json:[{"text":"🎲 Mystery Box","color":"light_purple"},{"text":" - ","color":"gray"},{"text":"Moving...","color":"yellow"}],priority:"conditional",freeze:5}
function #smithed.actionbar:message
""")

	write_versioned_function("zombies/mystery_box/on_hover", f"""
# Only over a usable box (active, any box during a Fire Sale, or a box with a pull in progress)
scoreboard players set #mb_usable {ns}.data 0
execute if entity @e[tag=bs.interaction.target,tag={ns}.mystery_box_active] run scoreboard players set #mb_usable {ns}.data 1
execute if score #zb_fire_sale_timer {ns}.data matches 1.. if entity @e[tag=bs.interaction.target,tag={ns}.mb_fs_active] run scoreboard players set #mb_usable {ns}.data 1
execute at @n[tag=bs.interaction.target] if entity @n[tag={ns}.mb_display,distance=..3] run scoreboard players set #mb_usable {ns}.data 1
execute if score #mb_usable {ns}.data matches 0 run return fail
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail

# Active box mid-move
execute if score #mb_move_timer {ns}.data matches 1.. if entity @e[tag=bs.interaction.target,tag={ns}.mystery_box_active] run return run function {ns}:v{version}/zombies/mystery_box/hud_moving

# This box's pull state (at the box)
execute at @n[tag=bs.interaction.target] run function {ns}:v{version}/zombies/mystery_box/hover_at_box
""")

	## Per-box hover state (@s = player, positioned at the box)
	write_versioned_function("zombies/mystery_box/hover_at_box", f"""
execute if entity @n[tag={ns}.mb_display,distance=..3,scores={{{ns}.mb.anim=1..}}] run return run function {ns}:v{version}/zombies/mystery_box/hud_spinning
# Ready: name the weapon waiting to be collected (read its item_name; fall back to a generic prompt)
data remove storage {ns}:temp _mb_hover_name
execute if entity @n[tag={ns}.mb_display,distance=..3] run data modify storage {ns}:temp _mb_hover_name set from entity @n[tag={ns}.mb_display,distance=..3] item.components."minecraft:item_name"
execute if entity @n[tag={ns}.mb_display,distance=..3] if data storage {ns}:temp _mb_hover_name run return run function {ns}:v{version}/zombies/mystery_box/hud_ready_named
execute if entity @n[tag={ns}.mb_display,distance=..3] run return run function {ns}:v{version}/zombies/mystery_box/hud_ready
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
# Remove all pull displays and presence boxes, reset all per-box state
kill @e[tag={ns}.mb_display]
kill @e[tag={ns}.mb_presence]
kill @e[tag={ns}.mb_temp]
scoreboard players set #mb_pulls {ns}.data 0
scoreboard players set #mb_move_timer {ns}.data 0
scoreboard players set #mb_fs_cleanup_pending {ns}.data 0
scoreboard players reset @a {ns}.mb.pid
scoreboard players set #mb_pid_counter {ns}.data 0
tag @e remove {ns}.mb_fs_active
tag @e remove {ns}.mb_orig_active
""")
