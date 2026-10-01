""" Right-click detection shared by every weapon path, including burst click tracking. """
# Imports
from beet import JsonFile
from stewbeet import (
	Advancement,
	ItemModifier,
	JsonDict,
	Mem,
	Predicate,
	set_json_encoder,
	write_versioned_function,
)

from ...config.stats.keys import BURST, RELOAD_TIME, REMAINING_BULLETS
from ..helpers.probes import Probe


# Functions
def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Right click detected through the using_item trigger.
	adv: JsonDict = {
		"criteria": {
			"requirement": {
				"trigger": "minecraft:using_item",
				"conditions": {
					"item": {
						"predicates": {
							"minecraft:custom_data": f"{{{ns}:{{gun:true}}}}"
						}
					}
				}
			}
		},
		"rewards": {
			"function": f"{ns}:v{version}/player/set_pending_clicks"
		}
	}
	Mem.ctx.data[ns].advancements[f"v{version}/right_click"] = set_json_encoder(Advancement(adv), max_level=-1)

	# The same click when an escort trader eats it: aiming at an entity sends an interact packet, and the item use only follows when
	# the interaction does not consume. The trader's empty offers return CONSUME, and handleInteract fires this trigger with the gun stack.
	adv_entity: JsonDict = {
		"criteria": {
			"requirement": {
				"trigger": "minecraft:player_interacted_with_entity",
				"conditions": {
					"item": {
						"predicates": {
							"minecraft:custom_data": f"{{{ns}:{{gun:true}}}}"
						}
					},
					# `entity` is a loot condition, so the entity predicate sits inside entity_properties; EntityPredicate keys its conditions
					# by registry id ("entity_type", "nbt"), and the old "type" makes the game reject the advancement.
					"entity": {
						"type": "minecraft:entity_properties",
						"entity": "this",
						"predicate": {
							"entity_type": "minecraft:wandering_trader",
							"nbt": f'{{Tags:["{ns}.zb_escort"]}}'
						}
					}
				}
			}
		},
		"rewards": {
			"function": f"{ns}:v{version}/player/set_pending_clicks_entity"
		}
	}
	Mem.ctx.data[ns].advancements[f"v{version}/right_click_entity"] = set_json_encoder(Advancement(adv_entity), max_level=-1)

	write_versioned_function("player/set_pending_clicks_entity", f"""
# Revoked, then the normal click path runs (it revokes its own).
advancement revoke @s only {ns}:v{version}/right_click_entity
function {ns}:v{version}/player/set_pending_clicks
""")

	write_versioned_function("player/set_pending_clicks", f"""
advancement revoke @s only {ns}:v{version}/right_click

# pending_clicks still >= 0 from last tick means the button is held.
execute if score @s {ns}.pending_clicks matches 0.. run scoreboard players set @s {ns}.held_click 1
execute if score @s {ns}.pending_clicks matches ..-1 run scoreboard players set @s {ns}.held_click 0

# A negative pending_clicks with a partial burst means the burst was interrupted (an auto-reload mid-burst);
# without this reset the mid-burst path keeps adding to a very negative count and the weapon never fires again.
execute if score @s {ns}.pending_clicks matches ..-1 run scoreboard players set @s {ns}.burst_count 0

scoreboard players set #is_mid_burst {ns}.data 0
execute if score @s {ns}.burst_count matches 1.. run function {ns}:v{version}/utils/copy_gun_data
execute if score @s {ns}.burst_count matches 1.. if data storage {ns}:gun all.stats{{fire_mode:"burst"}} run function {ns}:v{version}/player/check_mid_burst

# Mid-burst: add, to keep the burst going; otherwise set to 1 (held detection follows next tick if still held).
execute if score #is_mid_burst {ns}.data matches 1 run scoreboard players add @s {ns}.pending_clicks 1
execute unless score #is_mid_burst {ns}.data matches 1 run scoreboard players set @s {ns}.pending_clicks 1
""")

	write_versioned_function("player/check_mid_burst", f"""
execute store result score #burst_limit {ns}.data run data get storage {ns}:gun all.stats.{BURST}

execute if score @s {ns}.burst_count < #burst_limit {ns}.data run scoreboard players set #is_mid_burst {ns}.data 1
""")

	# Reading a path off a player serializes the whole player (inventory, ender chest, recipe book); bouncing the stack through
	# Bookshelf's forceloaded item_display measured 8x cheaper. Anything without {ns} custom data leaves the storage empty, as consumers expect.
	write_versioned_function("utils/copy_gun_data", f"""
data remove storage {ns}:gun all
data modify storage {ns}:gun SelectedItem set value {{id:""}}
execute unless items entity @s weapon.mainhand *[custom_data~{{{ns}:{{}}}}] run return 0
{Probe.item("weapon.mainhand")}
data modify storage {ns}:gun SelectedItem set from entity {Probe.ITEM_DISPLAY} item
data modify storage {ns}:gun all set from storage {ns}:gun SelectedItem.components."minecraft:custom_data".{ns}
""")

	write_versioned_function("player/tick", f"""
# Removed at the end of the tick.
tag @s add {ns}.ticking

# Once a second, and only if the player moved enough.
scoreboard players operation #acoustics_phase {ns}.data = #total_tick {ns}.data
scoreboard players operation #acoustics_phase {ns}.data %= #20 {ns}.data
execute if score #acoustics_phase {ns}.data matches 0 if predicate {ns}:v{version}/is_moving run function {ns}:v{version}/sound/compute_acoustics
execute if score #acoustics_phase {ns}.data matches 0 unless predicate {ns}:v{version}/is_on_ground run function {ns}:v{version}/sound/compute_acoustics

# The hand-swap key parks the weapon in the offhand to reload.
execute if items entity @s weapon.offhand * run function {ns}:v{version}/player/offhand_swap_check

# Dropping the weapon switches fire mode.
function {ns}:v{version}/switch/check_fire_mode_on_drop

function {ns}:v{version}/utils/copy_gun_data

# Before the zoom: a switch clears the old aim, so the new weapon's aim is decided after it.
function {ns}:v{version}/switch/main

function {ns}:v{version}/zoom/main

execute if score @s {ns}.cooldown > #total_tick {ns}.data if entity @s[tag={ns}.pump_sound] if data storage {ns}:gun all.sounds.pump run function {ns}:v{version}/sound/check/pump
execute unless score @s {ns}.cooldown > #total_tick {ns}.data if entity @s[tag={ns}.pump_sound] run tag @s remove {ns}.pump_sound

execute if score @s {ns}.cooldown > #total_tick {ns}.data if entity @s[tag={ns}.reload_mid_sound] if data storage {ns}:gun all.sounds.playermid run function {ns}:v{version}/sound/check/reload_mid
execute unless score @s {ns}.cooldown > #total_tick {ns}.data if entity @s[tag={ns}.reload_mid_sound] run tag @s remove {ns}.reload_mid_sound

execute if score @s {ns}.cooldown > #total_tick {ns}.data if data storage {ns}:gun all.sounds.playerend run function {ns}:v{version}/sound/check/reload_end
execute unless score @s {ns}.cooldown > #total_tick {ns}.data if entity @s[tag={ns}.reloading] run function {ns}:v{version}/ammo/end_reload

execute if score @s {ns}.pending_clicks matches -100.. run function {ns}:v{version}/player/right_click

# pending_clicks goes negative once the button is released.
execute if score @s {ns}.pending_clicks matches ..-1 run scoreboard players set @s {ns}.held_click 0

# Only once a burst is complete or the player switched weapons.
execute if score @s {ns}.pending_clicks matches ..-1 if score @s {ns}.burst_count matches 1.. run function {ns}:v{version}/player/reset_burst_if_complete

execute if data storage {ns}:gun all.gun run function {ns}:v{version}/actionbar/show

# Every 20 ticks mgs.dps is snapshotted into mgs.previous_dps and reset.
scoreboard players add @s {ns}.dps_timer 1
execute if score @s {ns}.dps_timer matches 20.. run function {ns}:v{version}/player/dps_snapshot

# instant_kill and infinite_ammo count down in real time.
execute if score @s {ns}.special.instant_kill matches 1.. run scoreboard players operation @s {ns}.special.instant_kill -= #tick_delta {ns}.data
execute if score @s {ns}.special.infinite_ammo matches 1.. run scoreboard players operation @s {ns}.special.infinite_ammo -= #tick_delta {ns}.data

tag @s remove {ns}.ticking

# The length of the item id string.
execute store result score @s {ns}.previous_selected run data get storage {ns}:gun SelectedItem.id
""")

	write_versioned_function("player/right_click", f"""
scoreboard players remove @s {ns}.pending_clicks 1

# 3 s after the last click, the lore and reserve ammo are refreshed.
execute if score @s {ns}.pending_clicks matches -60 if data storage {ns}:gun all.gun run function {ns}:v{version}/ammo/modify_lore {{slot:"weapon.mainhand"}}

execute if score @s {ns}.cooldown > #total_tick {ns}.data run return fail
execute if score @s {ns}.pending_clicks matches ..-1 run return fail

execute unless data storage {ns}:gun all.gun run return fail
execute unless score @s {ns}.special.infinite_ammo matches 1.. if score @s {ns}.{REMAINING_BULLETS} matches ..0 run return run function {ns}:v{version}/ammo/reload
""")

	# is_on_ground cannot be used: /tp @s ~ ~ ~ makes it false for two ticks.
	def json_enc[T: JsonFile](x: T) -> T: return set_json_encoder(x, max_level=-1)
	Mem.ctx.data[ns].predicates[f"v{version}/is_on_ground"] = json_enc(Predicate({"type":"minecraft:entity_properties","entity":"this","predicate":{"movement":{"vertical_speed":{"max":0.1}}}}))
	Mem.ctx.data[ns].predicates[f"v{version}/is_sprinting"] = json_enc(Predicate({"type":"minecraft:entity_properties","entity":"this","predicate":{"flags":{"is_sprinting":True}}}))
	Mem.ctx.data[ns].predicates[f"v{version}/is_sneaking"] = json_enc(Predicate({"type":"minecraft:entity_properties","entity":"this","predicate":{"flags":{"is_sneaking":True}}}))
	Mem.ctx.data[ns].predicates[f"v{version}/is_swimming"] = json_enc(Predicate({"type":"minecraft:entity_properties","entity":"this","predicate":{"flags":{"is_swimming":True}}}))
	Mem.ctx.data[ns].predicates[f"v{version}/is_moving"] = json_enc(Predicate({"type":"minecraft:entity_properties","entity":"this","predicate":{"movement":{"horizontal_speed":{"min":0.1}}}}))

	modifier: JsonDict = {"type":"minecraft:copy_custom_data","source":{"type":"minecraft:storage","source":f"{ns}:gun"},"ops":[{"source":"all.stats","target":f"{ns}.stats","op":"replace"}]}
	Mem.ctx.data[ns].item_modifiers[f"v{version}/update_stats"] = json_enc(ItemModifier(modifier))

	write_versioned_function("utils/update_model", """
$item modify entity @s weapon.mainhand {"type": "minecraft:set_components","components": {"minecraft:item_model": "$(item_model)"}}
""")

	# Hand swap (F) is a reload key (left click is the other, see weapon/left_click); the gun goes straight back, so the swap never shows.
	# Fire mode is on the drop key (switch).
	write_versioned_function("player/offhand_swap_check", f"""
# Main hand empty and a gun in the offhand.
execute unless items entity @s weapon.mainhand * if items entity @s weapon.offhand *[custom_data~{{{ns}:{{gun:true}}}}] run function {ns}:v{version}/player/swap_and_reload
""")

	write_versioned_function("player/swap_and_reload", f"""
item replace entity @s weapon.mainhand from entity @s weapon.offhand
item replace entity @s weapon.offhand with air

# Throwables carry {{gun:true}} but no {RELOAD_TIME}: ammo/reload would store a garbage cooldown from it and lock the item.
function {ns}:v{version}/utils/copy_gun_data
execute unless data storage {ns}:gun all.stats.{RELOAD_TIME} run return 0
function {ns}:v{version}/ammo/reload
""")

	write_versioned_function("player/reset_burst_if_complete", f"""
execute store result score #fire_mode_is_burst {ns}.data if data storage {ns}:gun all.stats{{fire_mode:"burst"}}

execute if score #fire_mode_is_burst {ns}.data matches 0 run scoreboard players set @s {ns}.burst_count 0
execute if score #fire_mode_is_burst {ns}.data matches 0 run return 0

execute store result score #burst_limit {ns}.data run data get storage {ns}:gun all.stats.burst
execute if score @s {ns}.burst_count >= #burst_limit {ns}.data run scoreboard players set @s {ns}.burst_count 0
""")

	write_versioned_function("player/dps_snapshot", f"""
scoreboard players operation @s {ns}.previous_dps = @s {ns}.dps
scoreboard players set @s {ns}.dps 0
scoreboard players set @s {ns}.dps_timer 0
""")

	# Run as the hit entity; the shooter is the ticking player. $(amount) is the damage float of the damage signal (24.0).
	write_versioned_function("weapon/dps_collect", f"""
# Stored as a float, read back x10 into integer tenths, the accumulator's unit.
$data modify storage {ns}:temp dps_amount set value $(amount)
execute store result score #sent_damage {ns}.data run data get storage {ns}:temp dps_amount 10
scoreboard players operation @n[tag={ns}.ticking] {ns}.dps += #sent_damage {ns}.data
""", tags=[f"{ns}:signals/damage"])

