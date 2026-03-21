
# ruff: noqa: E501
# Zombies Inventory Management
# Handles strict zombies slot layout, slot-tagged items, and recovery from moved/dropped items.
from stewbeet import Advancement, ItemModifier, JsonDict, Mem, set_json_encoder, write_versioned_function

from ...config.stats import ALL_SLOTS, CAPACITY, REMAINING_BULLETS


def generate_zombies_inventory() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	knife_cd = "{" + ns + ":{knife:true}}"
	zb_tagged_cd = "{" + ns + ":{zombies:{}}}"

	knife_slot_cd = "{" + ns + ":{knife:true,zombies:{hotbar:0}}}"
	gun_1_slot_cd = "{" + ns + ":{gun:true,zombies:{hotbar:1}}}"
	gun_2_slot_cd = "{" + ns + ":{gun:true,zombies:{hotbar:2}}}"
	gun_3_slot_cd = "{" + ns + ":{gun:true,zombies:{hotbar:3}}}"
	ability_slot_cd = "{" + ns + ":{zb_ability_item:true,zombies:{hotbar:4}}}"
	equipment_2_slot_cd = "{" + ns + ":{gun:true,zombies:{hotbar:6}}}"
	equipment_1_slot_cd = "{" + ns + ":{gun:true,zombies:{hotbar:7}}}"
	info_slot_cd = "{" + ns + ":{zb_info:true,zombies:{hotbar:8}}}"
	mag_1_slot_cd = "{" + ns + ":{magazine:true,zombies:{inventory:1}}}"
	mag_2_slot_cd = "{" + ns + ":{magazine:true,zombies:{inventory:2}}}"
	mag_3_slot_cd = "{" + ns + ":{magazine:true,zombies:{inventory:3}}}"

	knife_item = (
		f"minecraft:iron_sword[unbreakable={{}},custom_data={knife_cd},"
		f'item_name={{"text":"Knife","color":"white","italic":false}},'
		f'attribute_modifiers=[{{type:"attack_damage",amount:20,operation:"add_value",slot:"mainhand",id:"minecraft:base_attack_damage"}}]'
		f"]"
	)

	zb_tagged_match = f"*[custom_data~{zb_tagged_cd}]"
	equipment_1_match = f"*[custom_data~{equipment_1_slot_cd}]"

	zb_stats_modifier: JsonDict = {
		"function": "minecraft:copy_custom_data",
		"source": {"type": "minecraft:storage", "source": f"{ns}:temp"},
		"ops": [
			{"source": f"zb_item_stats.{CAPACITY}", "target": f"{ns}.stats.{CAPACITY}", "op": "replace"},
			{"source": f"zb_item_stats.{REMAINING_BULLETS}", "target": f"{ns}.stats.{REMAINING_BULLETS}", "op": "replace"},
		],
	}
	Mem.ctx.data[ns].item_modifiers[f"v{version}/zb_item_stats"] = set_json_encoder(ItemModifier(zb_stats_modifier), max_level=-1)

	zb_slot_modifier: JsonDict = {
		"function": "minecraft:copy_custom_data",
		"source": {"type": "minecraft:storage", "source": f"{ns}:temp"},
		"ops": [
			{"source": "zb_slot", "target": f"{ns}.zombies", "op": "replace"},
		],
	}
	Mem.ctx.data[ns].item_modifiers[f"v{version}/zb_slot_tag"] = set_json_encoder(ItemModifier(zb_slot_modifier), max_level=-1)

	all_slot_scans: str = ""
	for slot in ALL_SLOTS:
		all_slot_scans += (
			f'$execute if score #zb_inv_found {ns}.data matches 0 if items entity @s {slot} $(match) '
			f'run function {ns}:v{version}/zombies/inventory/move_found_slot {{from:"{slot}",to:"$(slot)"}}\n'
		)

	write_versioned_function("zombies/inventory/apply_slot_tag", f"""
data modify storage {ns}:temp zb_slot set value {{}}
$data modify storage {ns}:temp zb_slot.$(group) set value $(index)
$item modify entity @s $(slot) {ns}:v{version}/zb_slot_tag
""")

	write_versioned_function("zombies/inventory/read_mag_capacity", f"""
$item replace entity @s contents from entity @p[tag={ns}.zb_scaling_mag] $(slot)
execute store result score #zb_cap {ns}.data run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{CAPACITY}
kill @s
""")

	write_versioned_function("zombies/inventory/scale_magazine_slot", f"""
tag @s add {ns}.zb_scaling_mag
$execute summon item_display run function {ns}:v{version}/zombies/inventory/read_mag_capacity {{slot:"$(slot)"}}
tag @s remove {ns}.zb_scaling_mag

# Store face-value capacity directly (no consumable x8 scaling needed).
execute store result storage {ns}:temp zb_item_stats.{CAPACITY} int 1 run scoreboard players get #zb_cap {ns}.data

# Start at half capacity (floor).
scoreboard players set #zb_const {ns}.data 2
scoreboard players operation #zb_cap {ns}.data /= #zb_const {ns}.data
execute store result storage {ns}:temp zb_item_stats.{REMAINING_BULLETS} int 1 run scoreboard players get #zb_cap {ns}.data

$item modify entity @s $(slot) {ns}:v{version}/zb_item_stats
""")

	write_versioned_function("zombies/inventory/enforce_slot", f"""
$execute if items entity @s $(slot) $(match) run return 1

# If there is a slot-tagged zombies item in the wrong slot, drop it first then clear slot to avoid dupes.
$execute if items entity @s $(slot) {zb_tagged_match} run function {ns}:v{version}/zombies/inventory/drop_wrong_slot_item {{slot:"$(slot)"}}

scoreboard players set #zb_inv_found {ns}.data 0
{all_slot_scans}

execute if score #zb_inv_found {ns}.data matches 0 run tag @s add {ns}.inv_slot_owner
$execute if score #zb_inv_found {ns}.data matches 0 as @e[type=item,distance=..8,nbt={{Item:{{components:{{"minecraft:custom_data":$(expected_nbt)}}}}}}] on origin if entity @s[tag={ns}.inv_slot_owner] run function {ns}:v{version}/zombies/inventory/try_pick_dropped_item {{slot:"$(slot)",expected_nbt:$(expected_nbt)}}
execute if score #zb_inv_found {ns}.data matches 0 run tag @s remove {ns}.inv_slot_owner

return 0
""")

	write_versioned_function("zombies/inventory/move_found_slot", f"""
$execute if items entity @s $(to) * run function {ns}:v{version}/zombies/inventory/drop_wrong_slot_item {{slot:"$(to)"}}
$item replace entity @s $(to) from entity @s $(from)
$item replace entity @s $(from) with air
scoreboard players set #zb_inv_found {ns}.data 1
""")

	write_versioned_function("zombies/inventory/drop_wrong_slot_item", f"""
tag @s add {ns}.inv_slot_owner
summon minecraft:item ~ ~ ~ {{Item:{{id:"minecraft:stone",count:1}},Tags:["{ns}.inv_new_drop"]}}
$execute as @n[type=item,tag={ns}.inv_new_drop,distance=..1] run function {ns}:v{version}/zombies/inventory/copy_slot_item_to_drop {{slot:"$(slot)"}}
tag @s remove {ns}.inv_slot_owner
$item replace entity @s $(slot) with air
""")

	write_versioned_function("zombies/inventory/copy_slot_item_to_drop", f"""
$item replace entity @s contents from entity @p[tag={ns}.inv_slot_owner] $(slot)
data modify entity @s PickupDelay set value 0s
data modify entity @s Thrower set from entity @p[tag={ns}.inv_slot_owner] UUID
data modify entity @s Owner set from entity @s Thrower
tag @s remove {ns}.inv_new_drop
""")

	write_versioned_function("zombies/inventory/try_pick_dropped_item", f"""
$execute if score #zb_inv_found {ns}.data matches 0 run item replace entity @p[tag={ns}.inv_slot_owner] $(slot) from entity @n[type=item,distance=..8,nbt={{Item:{{components:{{"minecraft:custom_data":$(expected_nbt)}}}}}}] contents
$execute if score #zb_inv_found {ns}.data matches 0 run kill @n[type=item,distance=..8,nbt={{Item:{{components:{{"minecraft:custom_data":$(expected_nbt)}}}}}}]
scoreboard players set #zb_inv_found {ns}.data 1
""")

	write_versioned_function("zombies/inventory/give_starting_loadout", f"""
clear @s

# hotbar.0: knife
item replace entity @s hotbar.0 with {knife_item}
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.0",group:"hotbar",index:0}}

# hotbar.1 + inventory.1: starting weapon and scaled magazine
loot replace entity @s hotbar.1 loot {ns}:i/m1911
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.1",group:"hotbar",index:1}}

loot replace entity @s inventory.1 loot {ns}:i/m1911_mag
function {ns}:v{version}/zombies/inventory/scale_magazine_slot {{slot:"inventory.1"}}
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"inventory.1",group:"inventory",index:1}}

# hotbar.7: main equipment (frag by default)
data modify storage {ns}:temp zb_item_stats set value {{{CAPACITY}:4,{REMAINING_BULLETS}:4}}
loot replace entity @s hotbar.7 loot {ns}:i/frag_grenade
item modify entity @s hotbar.7 {ns}:v{version}/zb_item_stats
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.7",group:"hotbar",index:7}}

# hotbar.8: info item
function {ns}:v{version}/zombies/inventory/refresh_info_item

# hotbar.4: only for manual abilities (automatic abilities must not show this item)
execute if score @s {ns}.zb.ability matches 3.. run function {ns}:v{version}/zombies/inventory/give_ability_item
""")

	write_versioned_function("zombies/inventory/give_respawn_loadout", f"""
function {ns}:v{version}/zombies/inventory/give_starting_loadout
""")

	write_versioned_function("zombies/inventory/refresh_info_item", f"""
item replace entity @s hotbar.8 with minecraft:paper[custom_data={{{ns}:{{zb_info:true}}}},item_name={{"text":"\\u2139 Player Info","color":"gold","italic":false}},lore=[{{"text":"Round: ","color":"gray","italic":false,"extra":[{{"score":{{"name":"#zb_round","objective":"{ns}.data"}},"color":"gold"}}]}},{{"text":"Points: ","color":"gray","italic":false,"extra":[{{"score":{{"name":"@s","objective":"{ns}.zb.points"}},"color":"gold"}}]}},{{"text":"Kills: ","color":"gray","italic":false,"extra":[{{"score":{{"name":"@s","objective":"{ns}.zb.kills"}},"color":"green"}}]}},{{"text":"Downs: ","color":"gray","italic":false,"extra":[{{"score":{{"name":"@s","objective":"{ns}.zb.downs"}},"color":"red"}}]}},{{"text":"","italic":false}},{{"text":"Passive: ","color":"gray","italic":false,"extra":[{{"score":{{"name":"@s","objective":"{ns}.zb.passive"}},"color":"aqua"}}]}},{{"text":"Ability: ","color":"gray","italic":false,"extra":[{{"score":{{"name":"@s","objective":"{ns}.zb.ability"}},"color":"green"}}]}}]]
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.8",group:"hotbar",index:8}}
""")

	write_versioned_function("zombies/inventory/give_ability_item", f"""
item replace entity @s hotbar.4 with minecraft:paper[custom_data={{{ns}:{{zb_ability_item:true}}}},consumable={{consume_seconds:1000000,animation:"spear",sound:"minecraft:intentionally_empty",has_consume_particles:false}},food={{saturation:0,nutrition:0,can_always_eat:true}},use_effects={{can_sprint:true,speed_multiplier:1.0,interact_vibrations:false}},item_name={{"text":"Use Ability","color":"green","italic":false}},lore=[{{"text":"Right-click to activate","color":"gray","italic":false}}]]
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.4",group:"hotbar",index:4}}
""")

	write_versioned_function("zombies/inventory/replenish_grenades", f"""
execute unless items entity @s hotbar.7 {equipment_1_match} run return fail
execute store result score #nade_rem {ns}.data run data get entity @s Inventory[{{Slot:7b}}].components."minecraft:custom_data".{ns}.stats.{REMAINING_BULLETS}
scoreboard players add #nade_rem {ns}.data 2
execute if score #nade_rem {ns}.data matches 5.. run scoreboard players set #nade_rem {ns}.data 4

execute store result storage {ns}:temp zb_item_stats.{REMAINING_BULLETS} int 1 run scoreboard players get #nade_rem {ns}.data
data modify storage {ns}:temp zb_item_stats.{CAPACITY} set value 4
item modify entity @s hotbar.7 {ns}:v{version}/zb_item_stats
""")

	inv_changed_adv: JsonDict = {
		"criteria": {
			"change": {
				"trigger": "minecraft:inventory_changed",
			},
		},
		"rewards": {
			"function": f"{ns}:v{version}/zombies/inventory/on_change",
		},
	}
	Mem.ctx.data[ns].advancements[f"v{version}/zombies/inventory_changed"] = set_json_encoder(Advancement(inv_changed_adv), max_level=-1)

	write_versioned_function("zombies/inventory/on_change", f"""
advancement revoke @s only {ns}:v{version}/zombies/inventory_changed
execute unless score @s {ns}.zb.in_game matches 1 run return fail
execute if data storage {ns}:zombies game{{state:"lobby"}} run return fail
execute if data storage {ns}:zombies game{{state:"ended"}} run return fail

function {ns}:v{version}/zombies/inventory/check_slots
""")

	write_versioned_function("zombies/inventory/check_slots", f"""
# hard forbidden slot
execute if items entity @s hotbar.5 * run function {ns}:v{version}/zombies/inventory/drop_wrong_slot_item {{slot:"hotbar.5"}}

# Always-enforced slots
function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"hotbar.8",match:"*[custom_data~{info_slot_cd}]",expected_nbt:{info_slot_cd}}}
function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"hotbar.7",match:"*[custom_data~{equipment_1_slot_cd}]",expected_nbt:{equipment_1_slot_cd}}}
function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"hotbar.6",match:"*[custom_data~{equipment_2_slot_cd}]",expected_nbt:{equipment_2_slot_cd}}}
function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"hotbar.2",match:"*[custom_data~{gun_2_slot_cd}]",expected_nbt:{gun_2_slot_cd}}}
function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"hotbar.1",match:"*[custom_data~{gun_1_slot_cd}]",expected_nbt:{gun_1_slot_cd}}}
function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"hotbar.0",match:"*[custom_data~{knife_slot_cd}]",expected_nbt:{knife_slot_cd}}}
function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"inventory.1",match:"*[custom_data~{mag_1_slot_cd}]",expected_nbt:{mag_1_slot_cd}}}
function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"inventory.2",match:"*[custom_data~{mag_2_slot_cd}]",expected_nbt:{mag_2_slot_cd}}}

# Mule kick gates the third weapon/magazine slots only.
execute if score @s {ns}.zb.perk.mule_kick matches 1 run function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"hotbar.3",match:"*[custom_data~{gun_3_slot_cd}]",expected_nbt:{gun_3_slot_cd}}}
execute if score @s {ns}.zb.perk.mule_kick matches 1 run function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"inventory.3",match:"*[custom_data~{mag_3_slot_cd}]",expected_nbt:{mag_3_slot_cd}}}
execute unless score @s {ns}.zb.perk.mule_kick matches 1 run item replace entity @s hotbar.3 with air
execute unless score @s {ns}.zb.perk.mule_kick matches 1 run item replace entity @s inventory.3 with air

# Ability slot is only for manual abilities (automatic abilities such as coward should not show item)
execute if score @s {ns}.zb.ability matches 3.. run function {ns}:v{version}/zombies/inventory/enforce_slot {{slot:"hotbar.4",match:"*[custom_data~{ability_slot_cd}]",expected_nbt:{ability_slot_cd}}}
execute unless score @s {ns}.zb.ability matches 3.. run item replace entity @s hotbar.4 with air

# Clear cursor (prevent dragging tagged items outside managed inventory)
execute if items entity @s player.cursor * run function {ns}:v{version}/zombies/inventory/drop_wrong_slot_item {{slot:"player.cursor"}}
""")

	write_versioned_function("zombies/inventory/on_new_item", f"""
# Kill any non-zombies-slot managed drop from zombies players.
execute if data entity @s Item.components."minecraft:custom_data".{ns} on origin if score @s {ns}.zb.in_game matches 1 unless data entity @s Item.components."minecraft:custom_data".{ns}.zombies run kill @s
""", tags=["common_signals:signals/on_new_item"])

	write_versioned_function("zombies/inventory/recreate_critical_items", f"""
execute unless items entity @s hotbar.0 *[custom_data~{knife_slot_cd}] run item replace entity @s hotbar.0 with {knife_item}
execute unless items entity @s hotbar.0 *[custom_data~{knife_slot_cd}] run function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.0",group:"hotbar",index:0}}

execute unless items entity @s hotbar.7 *[custom_data~{equipment_1_slot_cd}] run loot replace entity @s hotbar.7 loot {ns}:i/frag_grenade
execute unless items entity @s hotbar.7 *[custom_data~{equipment_1_slot_cd}] run function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.7",group:"hotbar",index:7}}
execute unless items entity @s hotbar.7 *[custom_data~{equipment_1_slot_cd}] run data modify storage {ns}:temp zb_item_stats set value {{{CAPACITY}:4,{REMAINING_BULLETS}:0}}
execute unless items entity @s hotbar.7 *[custom_data~{equipment_1_slot_cd}] run item modify entity @s hotbar.7 {ns}:v{version}/zb_item_stats

execute unless items entity @s hotbar.8 *[custom_data~{info_slot_cd}] run function {ns}:v{version}/zombies/inventory/refresh_info_item
""")

