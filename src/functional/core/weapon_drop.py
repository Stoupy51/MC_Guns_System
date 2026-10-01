""" Shared on-death weapon drop.

A drop is a static item_display lying flat on the ground plus a small interaction hitbox that an in-game player can right-click to pick the gun up for 30 s.
Only the *capture* step differs per caller (a dying player's selected hotbar slot vs a dying mob's mainhand), so callers fill `{ns}:temp _dropw` (the gun item, no Slot tag) + `#drop_ammo {ns}.data`, then call `shared/drops/drop` positioned where the drop should fall from.

Used by multiplayer/drop_held_weapon (player deaths) and missions/drop_enemy_weapon (mob deaths).
"""
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from ...config.catalogs import PRIMARY_WEAPONS, SECONDARY_WEAPONS
from ...config.stats.keys import BASE_WEAPON, CAPACITY, GRENADE_TYPE, REMAINING_BULLETS
from ..helpers import MGS_TAG
from ..helpers.probes import Probe
from .feedback import ZombiesFeedback


# Classes
class WeaponDrop:
	""" Weapon drop helpers. """

	# Functions
	@staticmethod
	def weapon_drop_tick_lines(ns: str) -> str:
		""" Build the dropped-gun lifetime countdown (called from every mode's game_tick). """
		return f"""
# Drops count down in real time and expire.
execute as @e[type=minecraft:item_display,tag={ns}.dropped_gun] run scoreboard players operation @s {ns}.drop_timer -= #tick_delta {ns}.data
execute as @e[type=minecraft:interaction,tag={ns}.drop_int] run scoreboard players operation @s {ns}.drop_timer -= #tick_delta {ns}.data
kill @e[type=minecraft:item_display,tag={ns}.dropped_gun,scores={{{ns}.drop_timer=..0}}]
kill @e[type=minecraft:interaction,tag={ns}.drop_int,scores={{{ns}.drop_timer=..0}}]
""".strip()

	@staticmethod
	def write_shared_weapon_drop_functions() -> None:
		ns: str = Mem.ctx.project_id
		version: str = Mem.ctx.project_version

		write_load_file(f"""
# Ticks before a dropped gun despawns.
scoreboard objectives add {ns}.drop_timer dummy
""")

		## Run where the drop falls from (usually at the corpse). Callers set {ns}:temp _dropw to the gun item without its Slot tag,
		## and #drop_ammo {ns}.data to the bullet count to bake in (<= 0 means half a magazine: empty player guns, mob drops).
		write_versioned_function("shared/drops/drop", f"""
# Only guns drop.
execute unless data storage {ns}:temp _dropw.components."minecraft:custom_data".{ns}.gun run return 0
execute if data storage {ns}:temp _dropw.components."minecraft:custom_data".{ns}.stats.{GRENADE_TYPE} run return 0

# The held gun's own data only refreshes a few seconds after shooting stops, so the count is baked in; an empty gun drops at half capacity.
execute store result score #drop_half {ns}.data run data get storage {ns}:temp _dropw.components."minecraft:custom_data".{ns}.stats.{CAPACITY}
scoreboard players operation #drop_half {ns}.data /= #2 {ns}.data
execute if score #drop_ammo {ns}.data matches ..0 run scoreboard players operation #drop_ammo {ns}.data = #drop_half {ns}.data
execute store result storage {ns}:temp _dropw.components."minecraft:custom_data".{ns}.stats.{REMAINING_BULLETS} int 1 run scoreboard players get #drop_ammo {ns}.data

# Death drops embed a spare magazine at half capacity; swap drops never run this.
data modify storage {ns}:temp _dropmag_args set value {{}}
data modify storage {ns}:temp _dropmag_args.bw set from storage {ns}:temp _dropw.components."minecraft:custom_data".{ns}.stats.{BASE_WEAPON}
data remove storage {ns}:temp _dropmag
function {ns}:v{version}/shared/drops/mag_lookup
execute if data storage {ns}:temp _dropmag_args.mag run function {ns}:v{version}/shared/drops/capture_mag with storage {ns}:temp _dropmag_args
execute if data storage {ns}:temp _dropmag run data modify storage {ns}:temp _dropw.components."minecraft:custom_data".{ns}.drop_mag set from storage {ns}:temp _dropmag

# Bookshelf raycast straight down, so mid-air deaths drop on the first surface below.
data modify storage {ns}:input with set value {{}}
data modify storage {ns}:input with.blocks set value "function #bs.hitbox:callback/get_block_shape_with_fluid"
data modify storage {ns}:input with.piercing set value 0
data modify storage {ns}:input with.max_distance set value 100
data modify storage {ns}:input with.ignored_blocks set value "#{ns}:v{version}/empty"
data modify storage {ns}:input with.on_entry_point set value "function {ns}:v{version}/shared/drops/spawn"
scoreboard players set #drop_spawned {ns}.data 0
execute rotated ~ 90 run function #bs.raycast:run with storage {ns}:input

# Nothing below in range (over the void): drop where it died.
execute if score #drop_spawned {ns}.data matches 0 run function {ns}:v{version}/shared/drops/spawn
""")

		## Run at the raycast's ground hit point, or directly as the fallback; the item is in {ns}:temp _dropw.
		write_versioned_function("shared/drops/spawn", f"""
scoreboard players set #drop_spawned {ns}.data 1

# Lying flat (90° around X), with a random yaw so a batch of drops does not all face one way.
summon minecraft:item_display ~ ~0.05 ~ {{Tags:["{ns}.dropped_gun","{ns}.gm_entity","{ns}.drop_new"],item_display:"ground",transformation:{{left_rotation:[0.7071068f,0f,0f,0.7071068f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.75f,0.75f,0.75f]}}}}
data modify entity @n[tag={ns}.drop_new] item set from storage {ns}:temp _dropw
execute store result storage {ns}:temp _drop_yaw float 1 run random value -180..179
data modify entity @n[tag={ns}.drop_new] Rotation[0] set from storage {ns}:temp _drop_yaw
scoreboard players set @n[tag={ns}.drop_new] {ns}.drop_timer 600
tag @n[tag={ns}.drop_new] remove {ns}.drop_new

# Pickup hitbox (Bookshelf right-click).
summon minecraft:interaction ~ ~ ~ {{width:0.9f,height:0.6f,response:true,Tags:["{ns}.drop_int","{ns}.gm_entity","bs.entity.interaction","{ns}.drop_new"]}}
scoreboard players set @n[tag={ns}.drop_new] {ns}.drop_timer 600
execute as @n[tag={ns}.drop_new] run function #bs.interaction:on_right_click {{run:"function {ns}:v{version}/shared/drops/pickup",executor:"source"}}
tag @n[tag={ns}.drop_new] remove {ns}.drop_new
""")

		## base_weapon to magazine item id, and half a stack for consumable ammo.
		mag_lookup_lines: str = "\n".join(
			f'execute if data storage {ns}:temp _dropmag_args{{bw:"{w.item_id}"}} run '
			f'data modify storage {ns}:temp _dropmag_args merge value {{mag:"{w.magazine_id}",halfc:{max(1, w.default_mag_count // 2)}}}'
			for w in (*PRIMARY_WEAPONS, *SECONDARY_WEAPONS)
		)
		write_versioned_function("shared/drops/mag_lookup", mag_lookup_lines)

		## A fresh magazine from the item loot table into {ns}:temp _dropmag, at half capacity.
		write_versioned_function("shared/drops/capture_mag", f"""
summon minecraft:item_display ~ ~ ~ {{Tags:["{ns}.drop_mag_helper"]}}
$loot replace entity @n[tag={ns}.drop_mag_helper] contents loot {ns}:i/$(mag)
data modify storage {ns}:temp _dropmag set from entity @n[tag={ns}.drop_mag_helper] item
kill @n[tag={ns}.drop_mag_helper]
execute unless data storage {ns}:temp _dropmag run return 0

# Regular magazines: half their capacity.
execute store result score #mag_half {ns}.data run data get storage {ns}:temp _dropmag.components."minecraft:custom_data".{ns}.stats.{CAPACITY}
scoreboard players operation #mag_half {ns}.data /= #2 {ns}.data
execute if score #mag_half {ns}.data matches ..0 run scoreboard players set #mag_half {ns}.data 1
execute unless data storage {ns}:temp _dropmag.components."minecraft:custom_data".{ns}.consumable store result storage {ns}:temp _dropmag.components."minecraft:custom_data".{ns}.stats.{REMAINING_BULLETS} int 1 run scoreboard players get #mag_half {ns}.data

# Consumable ammo (stack count = bullets): half a stack.
$execute if data storage {ns}:temp _dropmag.components."minecraft:custom_data".{ns}.consumable run data modify storage {ns}:temp _dropmag.count set value $(halfc)
""")

		## Bookshelf callback, run as the clicking player, who must hold a gun in hotbar.1 or 2 (not the knife or grenades).
		## Missions players too: missions runs on multiplayer classes, with the same hotbar.
		write_versioned_function("shared/drops/pickup", f"""
execute unless score @s {ns}.mp.in_game matches 1 unless score @s {ns}.mi.in_game matches 1 run return fail
execute store result score #pick_sel {ns}.data run data get entity @s SelectedItemSlot
execute unless score #pick_sel {ns}.data matches 1..2 run return fail
execute unless items entity @s weapon.mainhand *[custom_data~{{{ns}:{{gun:true}}}}] run return fail
execute if data entity @s SelectedItem.components."minecraft:custom_data".{ns}.stats.{GRENADE_TYPE} run return fail
execute at @e[tag=bs.interaction.target] run function {ns}:v{version}/shared/drops/collect
""")

		## Run as the picker, at the drop: with 2 guns the held one is swapped, with 1 the drop fills the free slot.
		write_versioned_function("shared/drops/collect", f"""
execute unless entity @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] run return fail
execute store success score #pick_g0 {ns}.data if items entity @s hotbar.1 *[custom_data~{{{ns}:{{gun:true}}}}]
execute store success score #pick_g1 {ns}.data if items entity @s hotbar.2 *[custom_data~{{{ns}:{{gun:true}}}}]

# Without Overkill a pickup cannot leave two primaries.
scoreboard players set #pick_deny {ns}.data 0
function {ns}:v{version}/shared/drops/overkill_check
execute if score #pick_deny {ns}.data matches 1 run return fail

# Death drops hand their embedded spare magazine over and lose it.
execute if data entity @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] item.components."minecraft:custom_data".{ns}.drop_mag run function {ns}:v{version}/shared/drops/give_mag

execute if score #pick_g0 {ns}.data matches 1 if score #pick_g1 {ns}.data matches 1 run return run function {ns}:v{version}/shared/drops/swap
function {ns}:v{version}/shared/drops/take
""")

		## #is_primary from the base_weapon in {ns}:temp _isp.bw.
		is_primary_lines: str = "\n".join(
			f'execute if data storage {ns}:temp _isp{{bw:"{w.item_id}"}} run scoreboard players set #is_primary {ns}.data 1'
			for w in PRIMARY_WEAPONS
		)
		write_versioned_function("shared/drops/is_primary_lookup", f"""
scoreboard players set #is_primary {ns}.data 0
{is_primary_lines}
""")

		## Run as the picker, at the drop: denied when the result would be two primaries.
		write_versioned_function("shared/drops/overkill_check", f"""
# Only primary drops are restricted.
data modify storage {ns}:temp _isp set value {{}}
data modify storage {ns}:temp _isp.bw set from entity @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] item.components."minecraft:custom_data".{ns}.stats.{BASE_WEAPON}
function {ns}:v{version}/shared/drops/is_primary_lookup
execute if score #is_primary {ns}.data matches 0 run return 0

scoreboard players add @s {ns}.special.overkill 0
execute if score @s {ns}.special.overkill matches 1.. run return 0

# The slot keeping its gun: the held slot when taking, the other when swapping.
scoreboard players operation #pick_keep {ns}.data = #pick_sel {ns}.data
execute if score #pick_g0 {ns}.data matches 1 if score #pick_g1 {ns}.data matches 1 run scoreboard players set #pick_keep {ns}.data 1
execute if score #pick_g0 {ns}.data matches 1 if score #pick_g1 {ns}.data matches 1 run scoreboard players operation #pick_keep {ns}.data -= #pick_sel {ns}.data

data modify storage {ns}:temp _isp set value {{}}
execute if score #pick_keep {ns}.data matches 0 run {Probe.item("hotbar.0")}
execute if score #pick_keep {ns}.data matches 1 run {Probe.item("hotbar.1")}
execute if score #pick_keep {ns}.data matches 0..1 run data modify storage {ns}:temp _isp.bw set from entity {Probe.ITEM_DISPLAY} item.components."minecraft:custom_data".{ns}.stats.{BASE_WEAPON}
function {ns}:v{version}/shared/drops/is_primary_lookup
execute if score #is_primary {ns}.data matches 0 run return 0

scoreboard players set #pick_deny {ns}.data 1
tellraw @s [{MGS_TAG},{{"text":"You need the Overkill perk to carry two primary weapons.","color":"red"}}]
{ZombiesFeedback.zb_sound('deny')}
""")

		## One gun owned: the drop fills the other weapon slot.
		write_versioned_function("shared/drops/take", f"""
execute if score #pick_g0 {ns}.data matches 0 run item replace entity @s hotbar.1 from entity @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] contents
execute if score #pick_g0 {ns}.data matches 1 run item replace entity @s hotbar.2 from entity @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] contents
playsound minecraft:entity.item.pickup player @a[distance=..24] ~ ~ ~
kill @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3]
kill @e[tag=bs.interaction.target]
""")

		## Run as the picker, at the drop: the first free main inventory slot (inventory.0-26), never the hotbar.
		mag_slot_lines: str = "\n".join(
			f"execute if score #mag_slot {ns}.data matches -1 unless items entity @s inventory.{n} * run scoreboard players set #mag_slot {ns}.data {n}"
			for n in range(27)
		)
		write_versioned_function("shared/drops/give_mag", f"""
data modify storage {ns}:temp _give set value {{}}
data modify storage {ns}:temp _give.Item set from entity @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] item.components."minecraft:custom_data".{ns}.drop_mag
data modify storage {ns}:temp _give.Owner set from entity @s UUID

# So `item replace ... from entity` can read it.
summon minecraft:item_display ~ ~ ~ {{Tags:["{ns}.drop_mag_helper"]}}
data modify entity @n[tag={ns}.drop_mag_helper] item set from storage {ns}:temp _give.Item

scoreboard players set #mag_slot {ns}.data -1
{mag_slot_lines}
execute store result storage {ns}:temp _give.slot int 1 run scoreboard players get #mag_slot {ns}.data
execute if score #mag_slot {ns}.data matches 0.. run function {ns}:v{version}/shared/drops/place_mag with storage {ns}:temp _give

# Main inventory full: an owner-locked ground item (may land in the hotbar).
execute if score #mag_slot {ns}.data matches -1 at @s run function {ns}:v{version}/shared/drops/give_item with storage {ns}:temp _give

kill @n[tag={ns}.drop_mag_helper]
data remove entity @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] item.components."minecraft:custom_data".{ns}.drop_mag
""")

		## Macro key is only the slot (at most 27 variants).
		write_versioned_function("shared/drops/place_mag", f"""
$item replace entity @s inventory.$(slot) from entity @n[tag={ns}.drop_mag_helper] contents
""")

		## Zero delay, owner-locked, at the picker.
		write_versioned_function("shared/drops/give_item", f"""
$summon minecraft:item ~ ~0.2 ~ {{Item:$(Item),Owner:$(Owner),PickupDelay:0s,Tags:["{ns}.gm_entity"]}}
""")

		## The old gun becomes the new drop, with a fresh timer.
		write_versioned_function("shared/drops/swap", f"""
{Probe.item("hotbar.1")}
execute if score #pick_sel {ns}.data matches 2 run {Probe.item("hotbar.2")}
data modify storage {ns}:temp _swapw set from entity {Probe.ITEM_DISPLAY} item

# Held guns store remaining_bullets -1 (the live count is the score), so it is synced in.
execute store result storage {ns}:temp _swapw.components."minecraft:custom_data".{ns}.stats.{REMAINING_BULLETS} int 1 run scoreboard players get @s {ns}.{REMAINING_BULLETS}

execute if score #pick_sel {ns}.data matches 1 run item replace entity @s hotbar.1 from entity @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] contents
execute if score #pick_sel {ns}.data matches 2 run item replace entity @s hotbar.2 from entity @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] contents
data modify entity @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] item set from storage {ns}:temp _swapw
playsound minecraft:entity.item.pickup player @a[distance=..24] ~ ~ ~
scoreboard players set @n[type=minecraft:item_display,tag={ns}.dropped_gun,distance=..3] {ns}.drop_timer 600
scoreboard players set @n[type=minecraft:interaction,tag={ns}.drop_int,distance=..3] {ns}.drop_timer 600
""")

