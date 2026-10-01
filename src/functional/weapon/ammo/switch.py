""" Weapon switching: swap timing, weapon ids, and fire-mode toggling on drop. """
# Imports
from stewbeet import ItemModifier, JsonDict, Mem, set_json_encoder, write_versioned_function

from ....config.stats.keys import CAN_AUTO, CAN_BURST, FIRE_MODE, SWITCH, WEAPON_ID


# Functions
def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("switch/main", f"""
execute if data storage {ns}:gun all.gun unless data storage {ns}:gun all.stats.{WEAPON_ID} run function {ns}:v{version}/switch/set_weapon_id

# A different weapon than last tick starts the switch cooldown.
scoreboard players set #current_id {ns}.data 0
execute store result score #current_id {ns}.data run data get storage {ns}:gun all.stats.{WEAPON_ID}
execute unless score @s {ns}.last_selected = #current_id {ns}.data run function {ns}:v{version}/switch/on_weapon_switch

scoreboard players operation @s {ns}.last_selected = #current_id {ns}.data
""")

	write_versioned_function("switch/set_weapon_id", f"""
execute store result storage {ns}:gun all.stats.{WEAPON_ID} int 1 run scoreboard players add #next_id {ns}.data 1

# auto when the weapon supports it, else semi.
execute unless data storage {ns}:gun all.stats.{FIRE_MODE} if data storage {ns}:gun all.stats.{CAN_AUTO} run data modify storage {ns}:gun all.stats.{FIRE_MODE} set value "auto"
execute unless data storage {ns}:gun all.stats.{FIRE_MODE} unless data storage {ns}:gun all.stats.{CAN_AUTO} run data modify storage {ns}:gun all.stats.{FIRE_MODE} set value "semi"

item modify entity @s weapon.mainhand {ns}:v{version}/set_weapon_id
""")

	write_versioned_function("switch/on_weapon_switch", f"""
# Deferred reload: no ammo was consumed yet.
execute if entity @s[tag={ns}.reloading] run tag @s remove {ns}.reloading
execute if entity @s[tag={ns}.pump_sound] run tag @s remove {ns}.pump_sound
execute if entity @s[tag={ns}.reload_mid_sound] run tag @s remove {ns}.reload_mid_sound

# Zoomed on the previous weapon: clear the zoom score and slowness, or it stays stuck.
execute if score @s {ns}.zoom matches 1 run function {ns}:v{version}/zoom/clear_state

scoreboard players set @s {ns}.burst_count 0

execute store result score #cooldown {ns}.data run data get storage {ns}:gun all.stats.{SWITCH}

# quick_swap is a percentage (20 = 20% faster).
execute if score @s {ns}.special.quick_swap matches 1.. run function {ns}:v{version}/switch/apply_quick_swap

# As an expiry tick.
scoreboard players operation #cooldown {ns}.data += #total_tick {ns}.data
scoreboard players operation @s {ns}.cooldown = #cooldown {ns}.data

function {ns}:v{version}/switch/force_switch_animation

function {ns}:v{version}/ammo/compute_reserve

# Run as the player; weapon data in mgs:signals.
data modify storage {ns}:signals on_switch set value {{}}
data modify storage {ns}:signals on_switch.weapon set from storage {ns}:gun all
function #{ns}:signals/on_switch
""")

	write_versioned_function("switch/apply_quick_swap", f"""
# cooldown x (100 - quick_swap) / 100
scoreboard players operation #reduction {ns}.data = #100 {ns}.data
scoreboard players operation #reduction {ns}.data -= @s {ns}.special.quick_swap
scoreboard players operation #cooldown {ns}.data *= #reduction {ns}.data
scoreboard players operation #cooldown {ns}.data /= #100 {ns}.data

# At least 1 tick.
execute if score #cooldown {ns}.data matches ..0 run scoreboard players set #cooldown {ns}.data 1
""")

	write_versioned_function("switch/force_switch_animation", f"""
execute unless data storage {ns}:gun all.gun run return fail

# Attack speed follows the cooldown.
function {ns}:v{version}/switch/sync_attack_speed_with_cooldown

# Swaps when the item matches the previous one (26 chars = "minecraft:poisonous_potato").
execute store result score #current_length {ns}.data run data get storage {ns}:gun SelectedItem.id
execute if score #current_length {ns}.data = @s {ns}.previous_selected if score @s {ns}.previous_selected matches 26 run item modify entity @s weapon.mainhand {{"type": "minecraft:set_item","item": "minecraft:firework_star"}}
execute if score #current_length {ns}.data = @s {ns}.previous_selected unless score @s {ns}.previous_selected matches 26 run item modify entity @s weapon.mainhand {{"type": "minecraft:set_item","item": "minecraft:poisonous_potato"}}
""")

	write_versioned_function("switch/sync_attack_speed_with_cooldown", f"""
## attack_speed = 20.0 / cooldown - 4.0 (4.0 is the default), with 3 digits of precision.
scoreboard players operation #remaining_cooldown {ns}.data = @s {ns}.cooldown
scoreboard players operation #remaining_cooldown {ns}.data -= #total_tick {ns}.data
scoreboard players set #attack_speed {ns}.data 20000
scoreboard players operation #attack_speed {ns}.data /= #remaining_cooldown {ns}.data
scoreboard players remove #attack_speed {ns}.data 4000

# A temporary item_display edits the attribute modifier of the mainhand item.
tag @s add {ns}.to_modify
execute summon item_display run function {ns}:v{version}/switch/modify_attack_speed
tag @s remove {ns}.to_modify
""")

	write_versioned_function("switch/modify_attack_speed", f"""
item replace entity @s contents from entity @p[tag={ns}.to_modify] weapon.mainhand

execute unless data entity @s item.components."minecraft:attribute_modifiers" run data modify entity @s item.components."minecraft:attribute_modifiers" set value []
execute unless data entity @s item.components."minecraft:attribute_modifiers"[{{"type":"minecraft:attack_speed"}}] run data modify entity @s item.components."minecraft:attribute_modifiers" append value {{"type":"attack_speed","amount":0.0d,"operation":"add_value","slot":"mainhand","id":"minecraft:base_attack_speed"}}
execute store result entity @s item.components."minecraft:attribute_modifiers"[{{"type":"minecraft:attack_speed"}}].amount double 0.001 run scoreboard players get #attack_speed {ns}.data

# Enchantments stay hidden: this overwrites the whole component, and the item hides its empty-named mgs:left_click enchantment.
data modify entity @s item.components."minecraft:tooltip_display" set value {{"hide_tooltip":false,"hidden_components":["minecraft:attribute_modifiers","minecraft:enchantments"]}}

item replace entity @p[tag={ns}.to_modify] weapon.mainhand from entity @s contents

kill @s
""")

	# Drop key = fire mode. There is no key-press event, so the drop really happens (minecraft.drop stat) and is undone; reload is on hand swap and left click.
	write_versioned_function("switch/check_fire_mode_on_drop", f"""
execute if score @s {ns}.dropped matches 1.. run function {ns}:v{version}/switch/fire_mode_on_dropped_weapon
scoreboard players reset @s {ns}.dropped
""")

	write_versioned_function("switch/fire_mode_on_dropped_weapon", f"""
# The nearest dropped gun, only if the main hand is empty.
tag @s add {ns}.to_pickup
execute unless items entity @s weapon.mainhand * as @n[type=item,distance=..3,nbt={{Item:{{components:{{"minecraft:custom_data":{{{ns}:{{gun:true}}}}}}}}}}] run function {ns}:v{version}/switch/weapon_back_to_mainhand
tag @s remove {ns}.to_pickup

# The weapon is back in the main hand.
function {ns}:v{version}/utils/copy_gun_data

# Throwables carry a fire_mode but must not toggle.
execute unless data storage {ns}:gun all.stats.{CAN_AUTO} unless data storage {ns}:gun all.stats.{CAN_BURST} run return 0

# auto, semi, burst, auto, narrowed to what the weapon supports.
function {ns}:v{version}/switch/do_toggle_fire_mode
""")
	write_versioned_function("switch/weapon_back_to_mainhand", f"""
item replace entity @p[tag={ns}.to_pickup] weapon.mainhand from entity @s contents
kill @s
""")

	write_versioned_function("switch/do_toggle_fire_mode", f"""
function {ns}:v{version}/utils/copy_gun_data
data modify storage {ns}:temp fire_mode set from storage {ns}:gun all.stats.{FIRE_MODE}

execute store result score #has_auto {ns}.data if data storage {ns}:gun all.stats.{CAN_AUTO}
execute store result score #has_burst {ns}.data if data storage {ns}:gun all.stats.{CAN_BURST}

execute if score #has_auto {ns}.data matches 1 if score #has_burst {ns}.data matches 1 if data storage {ns}:temp {{fire_mode:"auto"}} run data modify storage {ns}:gun all.stats.{FIRE_MODE} set value "semi"
execute if score #has_auto {ns}.data matches 1 if score #has_burst {ns}.data matches 1 if data storage {ns}:temp {{fire_mode:"semi"}} run data modify storage {ns}:gun all.stats.{FIRE_MODE} set value "burst"
execute if score #has_auto {ns}.data matches 1 if score #has_burst {ns}.data matches 1 if data storage {ns}:temp {{fire_mode:"burst"}} run data modify storage {ns}:gun all.stats.{FIRE_MODE} set value "auto"

execute if score #has_auto {ns}.data matches 1 if score #has_burst {ns}.data matches 0 if data storage {ns}:temp {{fire_mode:"auto"}} run data modify storage {ns}:gun all.stats.{FIRE_MODE} set value "semi"
execute if score #has_auto {ns}.data matches 1 if score #has_burst {ns}.data matches 0 if data storage {ns}:temp {{fire_mode:"semi"}} run data modify storage {ns}:gun all.stats.{FIRE_MODE} set value "auto"

execute if score #has_auto {ns}.data matches 0 if score #has_burst {ns}.data matches 1 if data storage {ns}:temp {{fire_mode:"semi"}} run data modify storage {ns}:gun all.stats.{FIRE_MODE} set value "burst"
execute if score #has_auto {ns}.data matches 0 if score #has_burst {ns}.data matches 1 if data storage {ns}:temp {{fire_mode:"burst"}} run data modify storage {ns}:gun all.stats.{FIRE_MODE} set value "semi"

# Missing mode: auto when supported, else semi.
execute unless data storage {ns}:temp fire_mode if score #has_auto {ns}.data matches 1 run data modify storage {ns}:gun all.stats.{FIRE_MODE} set value "auto"
execute unless data storage {ns}:temp fire_mode if score #has_auto {ns}.data matches 0 run data modify storage {ns}:gun all.stats.{FIRE_MODE} set value "semi"

item modify entity @s weapon.mainhand {ns}:v{version}/set_fire_mode

# Run as the player; weapon and new mode in mgs:signals.
data modify storage {ns}:signals on_fire_mode_change set value {{}}
data modify storage {ns}:signals on_fire_mode_change.weapon set from storage {ns}:gun all
data modify storage {ns}:signals on_fire_mode_change.fire_mode set from storage {ns}:gun all.stats.{FIRE_MODE}
function #{ns}:signals/on_fire_mode_change

# @p would pay a needless distance sort.
playsound minecraft:block.note_block.hat ambient @s

# So the fire-mode highlight follows at once.
scoreboard players set @s {ns}.ab_force 1
""")

	modifier: JsonDict = {
		"type": "minecraft:copy_custom_data",
		"source": {
			"type": "minecraft:storage",
			"source": f"{ns}:gun"
		},
		"ops": [
			{
				"source": f"all.stats.{WEAPON_ID}",
				"target": f"{ns}.stats.{WEAPON_ID}",
				"op": "replace"
			}
		]
	}
	Mem.ctx.data[ns].item_modifiers[f"v{version}/set_weapon_id"] = set_json_encoder(ItemModifier(modifier), max_level=-1)

	modifier: JsonDict = {
		"type": "minecraft:copy_custom_data",
		"source": {
			"type": "minecraft:storage",
			"source": f"{ns}:gun"
		},
		"ops": [
			{
				"source": f"all.stats.{FIRE_MODE}",
				"target": f"{ns}.stats.{FIRE_MODE}",
				"op": "replace"
			}
		]
	}
	Mem.ctx.data[ns].item_modifiers[f"v{version}/set_fire_mode"] = set_json_encoder(ItemModifier(modifier), max_level=-1)

