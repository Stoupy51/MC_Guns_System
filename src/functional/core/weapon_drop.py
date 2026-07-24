
# ruff: noqa: E501
# Shared on-death weapon drop.
#
# A drop is a static item_display lying flat on the ground plus a small interaction hitbox that an
# in-game player can right-click to pick the gun up for 30 s. Only the *capture* step differs per
# caller (a dying player's selected hotbar slot vs a dying mob's mainhand), so callers fill
# `{ns}:temp _dropw` (the gun item, no Slot tag) + `#drop_ammo {ns}.data`, then call
# `shared/drops/drop` positioned where the drop should fall from.
#
# Used by multiplayer/drop_held_weapon (player deaths) and missions/drop_enemy_weapon (mob deaths).
from stewbeet import Mem, write_load_file, write_versioned_function

from ...config.catalogs import PRIMARY_WEAPONS, SECONDARY_WEAPONS
from ...config.stats import BASE_WEAPON, CAPACITY, GRENADE_TYPE, REMAINING_BULLETS
from ..helpers import MGS_TAG
from .feedback import zb_sound


def weapon_drop_tick_lines(ns: str) -> str:
	""" Build the dropped-gun lifetime countdown (called from every mode's game_tick). """
	return f"""
# Dropped-weapon lifetime: count down (real-time via #tick_delta) and remove expired drops
execute as @e[type=minecraft:item_display,tag={ns}.dropped_gun] run scoreboard players operation @s {ns}.drop_timer -= #tick_delta {ns}.data
execute as @e[type=minecraft:interaction,tag={ns}.drop_int] run scoreboard players operation @s {ns}.drop_timer -= #tick_delta {ns}.data
kill @e[type=minecraft:item_display,tag={ns}.dropped_gun,scores={{{ns}.drop_timer=..0}}]
kill @e[type=minecraft:interaction,tag={ns}.drop_int,scores={{{ns}.drop_timer=..0}}]
""".strip()


def write_shared_weapon_drop_functions() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_load_file(f"""
# Dropped-weapon lifetime (ticks remaining before a dropped gun despawns)
scoreboard objectives add {ns}.drop_timer dummy
""")

	## Drop entry point. Run positioned where the drop falls from (usually `at` the corpse).
	## Callers set {ns}:temp _dropw = the gun item without its Slot tag, and #drop_ammo {ns}.data to
	## the live bullet count to bake in (<= 0 means "half a magazine": empty player guns, mob drops).
	write_versioned_function("shared/drops/drop", f"""
# Only guns drop: knives, grenades and whatever else a capture step may have grabbed are ignored
execute unless data storage {ns}:temp _dropw.components."minecraft:custom_data".{ns}.gun run return 0
execute if data storage {ns}:temp _dropw.components."minecraft:custom_data".{ns}.stats.{GRENADE_TYPE} run return 0

# Bake the ammo count into the dropped item (a held gun's own custom data only refreshes a few
# seconds after shooting stops); an empty gun drops with 50% of its magazine capacity instead
execute store result score #drop_half {ns}.data run data get storage {ns}:temp _dropw.components."minecraft:custom_data".{ns}.stats.{CAPACITY}
scoreboard players operation #drop_half {ns}.data /= #2 {ns}.data
execute if score #drop_ammo {ns}.data matches ..0 run scoreboard players operation #drop_ammo {ns}.data = #drop_half {ns}.data
execute store result storage {ns}:temp _dropw.components."minecraft:custom_data".{ns}.stats.{REMAINING_BULLETS} int 1 run scoreboard players get #drop_ammo {ns}.data

# Death drops carry one spare magazine at 50% capacity, embedded in the gun's custom data
# (swap drops never run this, so a swapped-away gun is not halved and carries no free magazine)
data modify storage {ns}:temp _dropmag_args set value {{}}
data modify storage {ns}:temp _dropmag_args.bw set from storage {ns}:temp _dropw.components."minecraft:custom_data".{ns}.stats.{BASE_WEAPON}
data remove storage {ns}:temp _dropmag
function {ns}:v{version}/shared/drops/mag_lookup
execute if data storage {ns}:temp _dropmag_args.mag run function {ns}:v{version}/shared/drops/capture_mag with storage {ns}:temp _dropmag_args
execute if data storage {ns}:temp _dropmag run data modify storage {ns}:temp _dropw.components."minecraft:custom_data".{ns}.drop_mag set from storage {ns}:temp _dropmag

# Mid-air deaths: Bookshelf raycast straight down, the drop spawns on the first block surface below
data modify storage {ns}:input with set value {{}}
data modify storage {ns}:input with.blocks set value "function #bs.hitbox:callback/get_block_shape_with_fluid"
data modify storage {ns}:input with.piercing set value 0
data modify storage {ns}:input with.max_distance set value 100
data modify storage {ns}:input with.ignored_blocks set value "#{ns}:v{version}/empty"
data modify storage {ns}:input with.on_entry_point set value "function {ns}:v{version}/shared/drops/spawn"
scoreboard players set #drop_spawned {ns}.data 0
execute rotated ~ 90 run function #bs.raycast:run with storage {ns}:input

# Nothing below within range (died over the void) -> drop at the death position
execute if score #drop_spawned {ns}.data matches 0 run function {ns}:v{version}/shared/drops/spawn
""")

	## Spawn the drop entities at the current position (item in {ns}:temp _dropw)
	## Called as the raycast's on_entry_point (positioned at the ground hit point) or directly as a fallback
	write_versioned_function("shared/drops/spawn", f"""
scoreboard players set #drop_spawned {ns}.data 1

# Static item display lying flat on the ground (left_rotation = 90° around X), with a random yaw
# so a batch of drops doesn't end up all facing the same way
summon minecraft:item_display ~ ~0.05 ~ {{Tags:["{ns}.dropped_gun","{ns}.gm_entity","{ns}.drop_new"],item_display:"ground",transformation:{{left_rotation:[0.7071068f,0f,0f,0.7071068f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.75f,0.75f,0.75f]}}}}
data modify entity @n[tag={ns}.drop_new] item set from storage {ns}:temp _dropw
execute store result storage {ns}:temp _drop_yaw float 1 run random value -180..179
data modify entity @n[tag={ns}.drop_new] Rotation[0] set from storage {ns}:temp _drop_yaw
scoreboard players set @n[tag={ns}.drop_new] {ns}.drop_timer 600
tag @n[tag={ns}.drop_new] remove {ns}.drop_new

# Small interaction hitbox for pickup (Bookshelf right-click)
summon minecraft:interaction ~ ~ ~ {{width:0.9f,height:0.6f,response:true,Tags:["{ns}.drop_int","{ns}.gm_entity","bs.entity.interaction","{ns}.drop_new"]}}
scoreboard players set @n[tag={ns}.drop_new] {ns}.drop_timer 600
execute as @n[tag={ns}.drop_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/shared/drops/pickup",executor:"source"}}
tag @n[tag={ns}.drop_new] remove {ns}.drop_new
""")

	## Magazine lookup: base_weapon -> magazine item id + half of one full stack for consumable ammo
	mag_lookup_lines: str = "\n".join(
		f'execute if data storage {ns}:temp _dropmag_args{{bw:"{w.item_id}"}} run '
		f'data modify storage {ns}:temp _dropmag_args merge value {{mag:"{w.magazine_id}",halfc:{max(1, w.default_mag_count // 2)}}}'
		for w in (*PRIMARY_WEAPONS, *SECONDARY_WEAPONS)
	)
	write_versioned_function("shared/drops/mag_lookup", mag_lookup_lines)

	## Capture a fresh magazine from the item loot table into {ns}:temp _dropmag, filled to 50%
	write_versioned_function("shared/drops/capture_mag", f"""
summon minecraft:item_display ~ ~ ~ {{Tags:["{ns}.drop_mag_helper"]}}
$loot replace entity @n[tag={ns}.drop_mag_helper] contents loot {ns}:i/$(mag)
data modify storage {ns}:temp _dropmag set from entity @n[tag={ns}.drop_mag_helper] item
kill @n[tag={ns}.drop_mag_helper]
execute unless data storage {ns}:temp _dropmag run return 0

# Regular magazines: fill to 50% of their capacity (never a full magazine)
execute store result score #mag_half {ns}.data run data get storage {ns}:temp _dropmag.components."minecraft:custom_data".{ns}.stats.{CAPACITY}
scoreboard players operation #mag_half {ns}.data /= #2 {ns}.data
execute if score #mag_half {ns}.data matches ..0 run scoreboard players set #mag_half {ns}.data 1
execute unless data storage {ns}:temp _dropmag.components."minecraft:custom_data".{ns}.consumable store result storage {ns}:temp _dropmag.components."minecraft:custom_data".{ns}.stats.{REMAINING_BULLETS} int 1 run scoreboard players get #mag_half {ns}.data

# Consumable ammo (stack count = bullets): half of one full stack
$execute if data storage {ns}:temp _dropmag.components."minecraft:custom_data".{ns}.consumable run data modify storage {ns}:temp _dropmag.count set value $(halfc)
""")

	## Pickup (Bookshelf callback, @s = clicking player)
	## Requires holding a primary/secondary gun (hotbar.1/2, knife and grenades excluded).
	## Missions players are allowed too: missions runs on multiplayer classes, same hotbar layout.
	write_versioned_function("shared/drops/pickup", f"""
execute unless score @s {ns}.mp.in_game matches 1 unless score @s {ns}.mi.in_game matches 1 run return fail
execute store result score #pick_sel {ns}.data run data get entity @s SelectedItemSlot
execute unless score #pick_sel {ns}.data matches 1..2 run return fail
execute unless items entity @s weapon.mainhand *[custom_data~{{{ns}:{{gun:true}}}}] run return fail
execute if data entity @s SelectedItem.components."minecraft:custom_data".{ns}.stats.{GRENADE_TYPE} run return fail
execute at @e[tag=bs.interaction.target] run function {ns}:v{version}/shared/drops/collect
""")

	## Collect (@s = picker, positioned at the drop):
	## 2 guns -> swap the held gun with the drop; 1 gun -> take the drop into the free weapon slot
	write_versioned_function("shared/drops/collect", f"""
execute unless entity @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] run return fail
execute store success score #pick_g0 {ns}.data if items entity @s hotbar.1 *[custom_data~{{{ns}:{{gun:true}}}}]
execute store success score #pick_g1 {ns}.data if items entity @s hotbar.2 *[custom_data~{{{ns}:{{gun:true}}}}]

# Without the Overkill perk, a pickup may not leave the player with two primary weapons
scoreboard players set #pick_deny {ns}.data 0
function {ns}:v{version}/shared/drops/overkill_check
execute if score #pick_deny {ns}.data matches 1 run return fail

# Death drops carry a spare magazine inside the gun's custom data: hand it over and strip it from the gun
execute if data entity @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] item.components."minecraft:custom_data".{ns}.drop_mag run function {ns}:v{version}/shared/drops/give_mag

execute if score #pick_g0 {ns}.data matches 1 if score #pick_g1 {ns}.data matches 1 run return run function {ns}:v{version}/shared/drops/swap
function {ns}:v{version}/shared/drops/take
""")

	## Primary-weapon lookup: sets #is_primary from the base_weapon string in {ns}:temp _isp.bw
	is_primary_lines: str = "\n".join(
		f'execute if data storage {ns}:temp _isp{{bw:"{w.item_id}"}} run scoreboard players set #is_primary {ns}.data 1'
		for w in PRIMARY_WEAPONS
	)
	write_versioned_function("shared/drops/is_primary_lookup", f"""
scoreboard players set #is_primary {ns}.data 0
{is_primary_lines}
""")

	## Overkill gate (@s = picker, positioned at the drop): deny when the result would be two primaries
	write_versioned_function("shared/drops/overkill_check", f"""
# Only primary drops are restricted
data modify storage {ns}:temp _isp set value {{}}
data modify storage {ns}:temp _isp.bw set from entity @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] item.components."minecraft:custom_data".{ns}.stats.{BASE_WEAPON}
function {ns}:v{version}/shared/drops/is_primary_lookup
execute if score #is_primary {ns}.data matches 0 run return 0

# Overkill lets you carry two primary weapons
scoreboard players add @s {ns}.special.overkill 0
execute if score @s {ns}.special.overkill matches 1.. run return 0

# The slot that keeps its gun after this pickup: the held slot when taking, the other slot when swapping
scoreboard players operation #pick_keep {ns}.data = #pick_sel {ns}.data
execute if score #pick_g0 {ns}.data matches 1 if score #pick_g1 {ns}.data matches 1 run scoreboard players set #pick_keep {ns}.data 1
execute if score #pick_g0 {ns}.data matches 1 if score #pick_g1 {ns}.data matches 1 run scoreboard players operation #pick_keep {ns}.data -= #pick_sel {ns}.data

# If the kept gun is also a primary, deny the pickup
data modify storage {ns}:temp _isp set value {{}}
execute if score #pick_keep {ns}.data matches 0 run data modify storage {ns}:temp _isp.bw set from entity @s Inventory[{{Slot:0b}}].components."minecraft:custom_data".{ns}.stats.{BASE_WEAPON}
execute if score #pick_keep {ns}.data matches 1 run data modify storage {ns}:temp _isp.bw set from entity @s Inventory[{{Slot:1b}}].components."minecraft:custom_data".{ns}.stats.{BASE_WEAPON}
function {ns}:v{version}/shared/drops/is_primary_lookup
execute if score #is_primary {ns}.data matches 0 run return 0

scoreboard players set #pick_deny {ns}.data 1
tellraw @s [{MGS_TAG},{{"text":"You need the Overkill perk to carry two primary weapons.","color":"red"}}]
{zb_sound('deny')}
""")

	## Take: only one gun owned -> the drop fills the other weapon slot, then the drop is removed
	write_versioned_function("shared/drops/take", f"""
execute if score #pick_g0 {ns}.data matches 0 run item replace entity @s hotbar.1 from entity @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] contents
execute if score #pick_g0 {ns}.data matches 1 run item replace entity @s hotbar.2 from entity @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] contents
playsound minecraft:entity.item.pickup player @a[distance=..24] ~ ~ ~
kill @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3]
kill @e[tag=bs.interaction.target]
""")

	## Give the drop's embedded spare magazine to the picker (@s = picker, positioned at the drop)
	## The mag goes into the first free MAIN-inventory slot (inventory.0-26 excludes the hotbar):
	## the old ground-item give let vanilla pickup fill the hotbar first
	mag_slot_lines: str = "\n".join(
		f"execute if score #mag_slot {ns}.data matches -1 unless items entity @s inventory.{n} * run scoreboard players set #mag_slot {ns}.data {n}"
		for n in range(27)
	)
	write_versioned_function("shared/drops/give_mag", f"""
data modify storage {ns}:temp _give set value {{}}
data modify storage {ns}:temp _give.Item set from entity @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] item.components."minecraft:custom_data".{ns}.drop_mag
data modify storage {ns}:temp _give.Owner set from entity @s UUID

# Load the magazine into a helper display so `item replace ... from entity` can read it
summon minecraft:item_display ~ ~ ~ {{Tags:["{ns}.drop_mag_helper"]}}
data modify entity @n[tag={ns}.drop_mag_helper] item set from storage {ns}:temp _give.Item

# First free main-inventory slot
scoreboard players set #mag_slot {ns}.data -1
{mag_slot_lines}
execute store result storage {ns}:temp _give.slot int 1 run scoreboard players get #mag_slot {ns}.data
execute if score #mag_slot {ns}.data matches 0.. run function {ns}:v{version}/shared/drops/place_mag with storage {ns}:temp _give

# Main inventory full -> fall back to an owner-locked ground item (may land in the hotbar)
execute if score #mag_slot {ns}.data matches -1 at @s run function {ns}:v{version}/shared/drops/give_item with storage {ns}:temp _give

kill @n[tag={ns}.drop_mag_helper]
data remove entity @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] item.components."minecraft:custom_data".{ns}.drop_mag
""")

	## Place the magazine into the free main-inventory slot found above (macro key: slot only, <=27 variants)
	write_versioned_function("shared/drops/place_mag", f"""
$item replace entity @s inventory.$(slot) from entity @n[tag={ns}.drop_mag_helper] contents
""")

	## Zero-delay, owner-locked item entity at the picker's position
	write_versioned_function("shared/drops/give_item", f"""
$summon minecraft:item ~ ~0.2 ~ {{Item:$(Item),Owner:$(Owner),PickupDelay:0s,Tags:["{ns}.gm_entity"]}}
""")

	## Swap: capture the held gun, hand over the drop, then the old gun becomes the new drop (timer refreshed)
	write_versioned_function("shared/drops/swap", f"""
data modify storage {ns}:temp _swapw set from entity @s Inventory[{{Slot:1b}}]
execute if score #pick_sel {ns}.data matches 2 run data modify storage {ns}:temp _swapw set from entity @s Inventory[{{Slot:2b}}]
data remove storage {ns}:temp _swapw.Slot

# Held guns carry remaining_bullets:-1 in their item NBT (the live count is on the scoreboard), so sync it in
execute store result storage {ns}:temp _swapw.components."minecraft:custom_data".{ns}.stats.{REMAINING_BULLETS} int 1 run scoreboard players get @s {ns}.{REMAINING_BULLETS}

execute if score #pick_sel {ns}.data matches 1 run item replace entity @s hotbar.1 from entity @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] contents
execute if score #pick_sel {ns}.data matches 2 run item replace entity @s hotbar.2 from entity @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] contents
data modify entity @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] item set from storage {ns}:temp _swapw
playsound minecraft:entity.item.pickup player @a[distance=..24] ~ ~ ~
scoreboard players set @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] {ns}.drop_timer 600
scoreboard players set @n[type=minecraft:interaction,tag={ns}.drop_int,distance=..3] {ns}.drop_timer 600
""")

