
# ruff: noqa: E501
# Zombies Inventory Management
# Handles strict zombies slot layout, slot-tagged items, and recovery from moved/dropped items.
from stewbeet import Advancement, ItemModifier, JsonDict, Mem, set_json_encoder, write_versioned_function

from ...config.stats import ALL_SLOTS, CAPACITY, LETHAL_GRENADE_IDS, REMAINING_BULLETS
from ..helpers import knife_item_snbt
from .perks import PERK_DEFINITIONS, PERK_DESCRIPTIONS


def generate_zombies_inventory() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	gun_cd = "{" + ns + ":{gun:true}}"
	mag_cd = "{" + ns + ":{magazine:true}}"
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

	# Zombies keeps vanilla reach: its knife is the fallback weapon once ammo runs out
	knife_item = knife_item_snbt(ns)

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

	# Marks a magazine as zombies-converted by setting consumable to 2b.
	# Value 1b = true consumable (stack count = bullets), 2b = zombies non-consumable (custom_data only).
	zb_mark_converted_modifier: list[JsonDict] = [
		{
			"function": "minecraft:set_custom_data",
			"tag": f'{{{ns}: {{consumable: 2b}}}}',
		},
		{
			"function": "minecraft:set_components",
			"components": {"minecraft:max_stack_size": 1}
		}
	]
	Mem.ctx.data[ns].item_modifiers[f"v{version}/zb_mark_converted"] = set_json_encoder(ItemModifier(zb_mark_converted_modifier), max_level=-1) # type: ignore

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

	write_versioned_function("zombies/inventory/read_capacity", f"""
$item replace entity @s contents from entity @p[tag={ns}.zb_scaling_mag] $(slot)
$execute store result score #zb_cap {ns}.data run data get entity @s item.components."minecraft:custom_data".{ns}.stats.{CAPACITY} $(multiplier)
kill @s
""")

	write_versioned_function("zombies/inventory/scale_magazine_slot", f"""
# Read capacity from the paired weapon at hotbar.$(index) (inventory.N always pairs with hotbar.N)
tag @s add {ns}.zb_scaling_mag
$execute summon item_display run function {ns}:v{version}/zombies/inventory/read_capacity {{slot:"hotbar.$(index)",multiplier:6}}
tag @s remove {ns}.zb_scaling_mag

# Write capacity and starting ammo into custom_data
execute store result storage {ns}:temp zb_item_stats.{CAPACITY} int 1 run scoreboard players get #zb_cap {ns}.data
$execute store result storage {ns}:temp zb_item_stats.{REMAINING_BULLETS} int $(remaining_multiplier) run scoreboard players get #zb_cap {ns}.data
$item modify entity @s $(slot) {ns}:v{version}/zb_item_stats

# Mark as zombies-converted (consumable=2b): ammo.py reads remaining_bullets instead of stack count.
$item modify entity @s $(slot) {ns}:v{version}/zb_mark_converted

# Force count to 1 (consumable magazines used stack count as ammo, now using custom_data)
scoreboard players set #bullets {ns}.data 1
$item modify entity @s $(slot) {ns}:v{version}/set_consumable_count

# Update magazine lore to show new ammo count
data modify storage {ns}:temp {CAPACITY} set from storage {ns}:temp zb_item_stats.{CAPACITY}
execute store result score #bullets {ns}.data run data get storage {ns}:temp zb_item_stats.{REMAINING_BULLETS}
$function {ns}:v{version}/ammo/modify_mag_lore {{slot:"$(slot)"}}
""")

	write_versioned_function("zombies/inventory/enforce_slot", f"""
$execute if items entity @s $(slot) $(match) run return 1

# Scan all inventory slots for the correct item and swap it into place
scoreboard players set #zb_inv_found {ns}.data 0
{all_slot_scans}
execute if score #zb_inv_found {ns}.data matches 1 run return 1

# Not found in any slot: drop wrong zombies item from target slot if present, then try ground pickup
$execute if items entity @s $(slot) {zb_tagged_match} run function {ns}:v{version}/zombies/inventory/drop_wrong_slot_item {{slot:"$(slot)"}}

tag @s add {ns}.inv_slot_owner
$execute as @e[type=item,distance=..8,nbt={{Item:{{components:{{"minecraft:custom_data":$(expected_nbt)}}}}}}] on origin if entity @s[tag={ns}.inv_slot_owner] run function {ns}:v{version}/zombies/inventory/try_pick_dropped_item {{slot:"$(slot)",expected_nbt:$(expected_nbt)}}
tag @s remove {ns}.inv_slot_owner

return 0
""")

	write_versioned_function("zombies/inventory/move_found_slot", f"""
# Swap source and target via temp item_display (handles empty target too)
tag @s add {ns}.inv_swapping
$execute summon item_display run function {ns}:v{version}/zombies/inventory/swap_slots {{from:"$(from)",to:"$(to)"}}
tag @s remove {ns}.inv_swapping
scoreboard players set #zb_inv_found {ns}.data 1
""")

	write_versioned_function("zombies/inventory/swap_slots", f"""
# @s = temp item_display, player = @p[tag={ns}.inv_swapping]
# Save target item to temp display
$item replace entity @s contents from entity @p[tag={ns}.inv_swapping] $(to)
# Move source to target
$item replace entity @p[tag={ns}.inv_swapping] $(to) from entity @p[tag={ns}.inv_swapping] $(from)
# Put old target item (from display) into source, or clear source if target was empty
$execute if items entity @s contents * run item replace entity @p[tag={ns}.inv_swapping] $(from) from entity @s contents
$execute unless items entity @s contents * run item replace entity @p[tag={ns}.inv_swapping] $(from) with air
kill @s
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
function {ns}:v{version}/zombies/inventory/scale_magazine_slot {{slot:"inventory.1",index:1,remaining_multiplier:0.5}}
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"inventory.1",group:"inventory",index:1}}

# hotbar.7: main equipment (frag by default). Record the lethal type so an empty slot later
# refills with frag (index 0), not some stale value from a previous life.
loot replace entity @s hotbar.7 loot {ns}:i/frag_grenade
item modify entity @s hotbar.7 {ns}:v{version}/grenade/set_count_4
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.7",group:"hotbar",index:7}}
scoreboard players set @s {ns}.zb.lethal_type 0

# hotbar.8: info item
function {ns}:v{version}/zombies/inventory/refresh_info_item

# hotbar.4: only for manual abilities (automatic abilities must not show this item)
execute if score @s {ns}.zb.ability matches 3.. run function {ns}:v{version}/zombies/inventory/give_ability_item
""")

	write_versioned_function("zombies/inventory/give_respawn_loadout", f"""
function {ns}:v{version}/zombies/inventory/give_starting_loadout

# Bleed-out respawns come back lighter than a fresh game start: knife + M1911 + only 2 frags.
# The starting-loadout clear also strips any bought knife/grenade-type/tactical (intended).
item modify entity @s hotbar.7 {ns}:v{version}/grenade/set_count_2
""")

	# Perk list for the info paper (one lore line per owned perk, themed by perk color).
	perk_count_lines: str = "\n".join(
		f"execute if score @s {ns}.zb.perk.{pid} matches 1 run scoreboard players add #info_perk_count {ns}.data 1"
		for pid in PERK_DEFINITIONS
	)
	perk_item_lines: str = "\n".join(
		f'execute if score @s {ns}.zb.perk.{pid} matches 1 run data modify storage {ns}:temp info.lore append value {{"text":"\\u2022 {pdata["display_name"]}","color":"{pdata["text_color"]}","italic":false}}'
		for pid, pdata in PERK_DEFINITIONS.items()
	)
	write_versioned_function("zombies/inventory/refresh_info_item", f"""
# Resolve scoreboard values into storage so lore lines render concrete numbers.
execute store result storage {ns}:temp info.round int 1 run scoreboard players get #zb_round {ns}.data
execute store result storage {ns}:temp info.points int 1 run scoreboard players get @s {ns}.zb.points
execute store result storage {ns}:temp info.kills int 1 run scoreboard players get @s {ns}.zb.kills
execute store result storage {ns}:temp info.downs int 1 run scoreboard players get @s {ns}.zb.downs

# Build the base lore list with baked numbers, then append a line per owned perk.
function {ns}:v{version}/zombies/inventory/build_info_lore with storage {ns}:temp info
scoreboard players set #info_perk_count {ns}.data 0
{perk_count_lines}
execute if score #info_perk_count {ns}.data matches 1.. run data modify storage {ns}:temp info.lore append value {{"text":"","italic":false}}
execute if score #info_perk_count {ns}.data matches 1.. run data modify storage {ns}:temp info.lore append value {{"text":"Perks:","color":"light_purple","italic":false}}
{perk_item_lines}

function {ns}:v{version}/zombies/inventory/refresh_info_item_render with storage {ns}:temp info
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.8",group:"hotbar",index:8}}

# Keep the perk display items (inventory.26 and down) in sync with the same cadence
function {ns}:v{version}/zombies/inventory/refresh_perk_items
""")

	# Macro: build the 4 base lore lines (with concrete numbers) as an NBT list.
	write_versioned_function("zombies/inventory/build_info_lore", f"""
$data modify storage {ns}:temp info.lore set value [{{"text":"Round: $(round)","color":"gray","italic":false}},{{"text":"Points: $(points)","color":"gray","italic":false}},{{"text":"Kills: $(kills)","color":"gray","italic":false}},{{"text":"Downs: $(downs)","color":"gray","italic":false}}]
""")

	# Macro: render the paper with the pre-built lore list ($(lore) substitutes the list SNBT).
	write_versioned_function("zombies/inventory/refresh_info_item_render", f"""
$item replace entity @s hotbar.8 with minecraft:paper[custom_data={{{ns}:{{zb_info:true}}}},item_name=["",{{"text":"\\u2139 ","italic":false}},{{"text":"Player Info","color":"gold","italic":false}}],lore=$(lore)]
""")

	# Perk display items: one mini perk-machine item per owned perk, on the LAST main inventory row.
	# custom_data has NO "zombies" key on purpose: on_new_item kills any {ns}-tagged drop without it,
	# so a thrown perk item silently despawns and reappears on the next refresh.
	#
	# PERF: each perk owns a FIXED slot (26 - its index) instead of packing from 26 down. This keeps
	# placement fully STATIC — no per-slot macro (the old place_perk_at was a dynamic `with storage`
	# macro whose slot varied, so it missed the macro cache and re-parsed a ~250-char item string on
	# every call) and no clear-all-then-place-all churn. refresh now writes the inventory only when a
	# perk is actually gained or lost: steady state (incl. the 5s cadence + on_new_perk on a re-grant
	# of an already-shown perk) is just cheap score / `if items` checks with zero item mutations.
	# Trade-off: unowned perks leave a gap rather than the row staying packed.
	perk_display_lines: list[str] = []
	for i, (pid, pdata) in enumerate(PERK_DEFINITIONS.items()):
		slot: int = 26 - i
		lore_parts: list[str] = [
			f'{{"text":"{line}","color":"gray","italic":false}}'
			for line in PERK_DESCRIPTIONS.get(pid, [])
		]
		lore_parts.append('{"text":"Owned perk","color":"dark_gray","italic":false}')
		lore_snbt: str = "[" + ",".join(lore_parts) + "]"
		perk_item: str = (
			f'minecraft:paper[item_model="{ns}:perk_machine_{pid}",'
			f"custom_data={{{ns}:{{zb_perk_display:true}}}},"
			f'item_name={{"text":"{pdata["display_name"]}","color":"{pdata["text_color"]}","italic":false}},'
			f"lore={lore_snbt}]"
		)
		# Owned but not yet shown -> place it once. Not owned but a stale display is here -> clear it.
		perk_display_lines.append(
			f"execute if score @s {ns}.zb.perk.{pid} matches 1 unless items entity @s inventory.{slot} "
			f"*[custom_data~{{{ns}:{{zb_perk_display:true}}}}] run item replace entity @s inventory.{slot} with {perk_item}"
		)
		perk_display_lines.append(
			f"execute unless score @s {ns}.zb.perk.{pid} matches 1 if items entity @s inventory.{slot} "
			f"*[custom_data~{{{ns}:{{zb_perk_display:true}}}}] run item replace entity @s inventory.{slot} with air"
		)
	perk_display_sync: str = "\n".join(perk_display_lines)
	# Tagged into the on_new_perk signal (@s = buying player) so a purchase shows up instantly.
	write_versioned_function("zombies/inventory/refresh_perk_items", f"""
# Diff each perk's fixed slot against ownership: place a newly-gained perk, clear a lost one, and
# leave already-correct slots untouched (no inventory writes in steady state).
{perk_display_sync}
""", tags=[f"{ns}:zombies/on_new_perk"])

	write_versioned_function("zombies/inventory/give_ability_item", f"""
item replace entity @s hotbar.4 with minecraft:paper[custom_data={{{ns}:{{zb_ability_item:true}}}},consumable={{consume_seconds:1000000,animation:"spear",sound:"minecraft:intentionally_empty",has_consume_particles:false}},food={{saturation:0,nutrition:0,can_always_eat:true}},use_effects={{can_sprint:true,speed_multiplier:1.0,interact_vibrations:false}},item_name={{"text":"Use Ability","color":"green","italic":false}},lore=[{{"text":"Right-click to activate","color":"gray","italic":false}}]]
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.4",group:"hotbar",index:4}}
""")

	write_versioned_function("zombies/inventory/replenish_grenades", f"""
# Case 1: player already has grenades in slot 7 - add 2, cap at 4
execute if items entity @s hotbar.7 {equipment_1_match} run item modify entity @s hotbar.7 {ns}:v{version}/grenade/set_count_add_2
execute if items entity @s hotbar.7 {equipment_1_match} store result score #nade_count {ns}.data run data get entity @s Inventory[{{Slot:7b}}].count
execute if items entity @s hotbar.7 {equipment_1_match} if score #nade_count {ns}.data matches 5.. run item modify entity @s hotbar.7 {ns}:v{version}/grenade/set_count_4
execute if items entity @s hotbar.7 {equipment_1_match} run return 0

# Case 2: slot 7 is empty (used all grenades) - give 2 of the player's BOUGHT lethal type, not a
# hardcoded frag (a player who bought semtex and used them all should get 2 semtex back).
execute unless items entity @s hotbar.7 * run function {ns}:v{version}/zombies/inventory/give_lethal_type {{count:2}}
""")

	# Re-give the player's recorded lethal type (frag / semtex / …) into the empty hotbar.7. The
	# per-player {ns}.zb.lethal_type score is set on give (starting loadout = frag) and on a lethal
	# wall-buy (wallbuys.py). frag is the fallback for an unset/0 score.
	# Widow's Wine owners always get web grenades in the lethal slot, regardless of the recorded
	# lethal type — so every refill path (respawn replenish, Max Ammo, give_lethal_type) hands out
	# webs. `return run` short-circuits the frag/semtex fallback below.
	lethal_loot_lines: str = f"execute if score @s {ns}.special.widows_wine matches 1 run return run loot replace entity @s hotbar.7 loot {ns}:i/web_grenade\n"
	lethal_loot_lines += f"execute unless score @s {ns}.zb.lethal_type matches 1.. run loot replace entity @s hotbar.7 loot {ns}:i/{LETHAL_GRENADE_IDS[0]}\n"
	lethal_loot_lines += "\n".join(
		f"execute if score @s {ns}.zb.lethal_type matches {i} run loot replace entity @s hotbar.7 loot {ns}:i/{gid}"
		for i, gid in enumerate(LETHAL_GRENADE_IDS) if i > 0
	)
	write_versioned_function("zombies/inventory/loot_replace_lethal", lethal_loot_lines)

	# Fill hotbar.7 with $(count) grenades of the player's lethal type, then re-tag the slot.
	write_versioned_function("zombies/inventory/give_lethal_type", f"""
function {ns}:v{version}/zombies/inventory/loot_replace_lethal
$item modify entity @s hotbar.7 {ns}:v{version}/grenade/set_count_$(count)
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.7",group:"hotbar",index:7}}
""")

	# Record the player's lethal type from a wall-buy (called by wallbuys.py buy_lethal after the
	# new-purchase give). Reads the bought weapon_id out of the {ns}:temp _wb_weapon storage.
	lethal_record_lines: str = "\n".join(
		f'execute if data storage {ns}:temp _wb_weapon{{weapon_id:"{gid}"}} run scoreboard players set @s {ns}.zb.lethal_type {i}'
		for i, gid in enumerate(LETHAL_GRENADE_IDS) if i > 0
	)
	write_versioned_function("zombies/inventory/record_lethal_type", f"""
scoreboard players set @s {ns}.zb.lethal_type 0
{lethal_record_lines}
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

# Prevent recursive re-entry (item replace in swap/enforce can re-trigger inventory_changed)
execute if entity @s[tag={ns}.inv_checking] run return fail
tag @s add {ns}.inv_checking
function {ns}:v{version}/zombies/inventory/check_slots
tag @s remove {ns}.inv_checking
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

# Clean orphaned magazines (gun lost in PAP but magazine remains) — skip slots actively in PAP
execute unless score @s {ns}.zb.pap_s matches 1 unless items entity @s hotbar.1 *[custom_data~{gun_cd}] if items entity @s inventory.1 *[custom_data~{mag_cd}] run item replace entity @s inventory.1 with air
execute unless score @s {ns}.zb.pap_s matches 2 unless items entity @s hotbar.2 *[custom_data~{gun_cd}] if items entity @s inventory.2 *[custom_data~{mag_cd}] run item replace entity @s inventory.2 with air
execute unless score @s {ns}.zb.pap_s matches 3 unless items entity @s hotbar.3 *[custom_data~{gun_cd}] if items entity @s inventory.3 *[custom_data~{mag_cd}] run item replace entity @s inventory.3 with air
""")

	write_versioned_function("zombies/game_tick", f"""
# Refresh player info item every 5 seconds (100 ticks)
scoreboard players add #zb_info_timer {ns}.data 1
execute if score #zb_info_timer {ns}.data matches 100.. run scoreboard players set #zb_info_timer {ns}.data 0
execute if score #zb_info_timer {ns}.data matches 0 as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] if items entity @s hotbar.8 *[custom_data~{info_slot_cd}] run function {ns}:v{version}/zombies/inventory/refresh_info_item
""")

	write_versioned_function("zombies/inventory/on_new_item", f"""
# Kill any non-zombies-slot managed drop from zombies players.
execute if data entity @s Item.components."minecraft:custom_data".{ns} on origin if score @s {ns}.zb.in_game matches 1 unless data entity @s Item.components."minecraft:custom_data".{ns}.zombies run kill @s
""", tags=["common_signals:signals/on_new_item"])

	write_versioned_function("zombies/inventory/recreate_critical_items", f"""
execute unless items entity @s hotbar.0 *[custom_data~{knife_slot_cd}] run item replace entity @s hotbar.0 with {knife_item}
execute unless items entity @s hotbar.0 *[custom_data~{knife_slot_cd}] run function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.0",group:"hotbar",index:0}}

execute unless items entity @s hotbar.7 *[custom_data~{equipment_1_slot_cd}] run function {ns}:v{version}/zombies/inventory/loot_replace_lethal
execute unless items entity @s hotbar.7 *[custom_data~{equipment_1_slot_cd}] run function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.7",group:"hotbar",index:7}}

execute unless items entity @s hotbar.8 *[custom_data~{info_slot_cd}] run function {ns}:v{version}/zombies/inventory/refresh_info_item
""")
