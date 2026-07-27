""" The info paper: its lore, its perk lines and the perk display items beside it. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ...machines.perks.definitions import PERK_DEFINITIONS, PERK_DESCRIPTIONS


# Functions
def write_info_item() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Perk list for the info paper (one lore line per owned perk, themed by perk color).
	perk_count_lines: str = "\n".join(
		f"execute if score @s {ns}.zb.perk.{pid} matches 1 run scoreboard players add #info_perk_count {ns}.data 1"
		for pid in PERK_DEFINITIONS
	)
	perk_item_lines: str = "\n".join(
		f'execute if score @s {ns}.zb.perk.{pid} matches 1 run data modify storage {ns}:temp info.lore append value {{"text":"\\u2022 {pdata.display_name}","color":"{pdata.text_color}","italic":false}}'
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
	# custom_data has NO "zombies" key on purpose: on_new_item kills any {ns}-tagged drop without it.
	# A thrown perk item therefore despawns silently and reappears on the next refresh.
	#
	# PERF: each perk owns a FIXED slot (26 - its index) instead of packing from 26 down.
	# That keeps placement fully STATIC, with no per-slot macro.
	# The old place_perk_at was a dynamic `with storage` macro whose slot varied, so it missed the macro cache and re-parsed a ~250-char item string every call.
	# It also avoids clear-all-then-place-all churn: refresh now writes the inventory only when a perk is gained or lost.
	# Steady state is just cheap score and `if items` checks with zero item mutations.
	# Trade-off: unowned perks leave a gap rather than the row staying packed.
	perk_display_lines: list[str] = []
	for i, (pid, pdata) in enumerate(PERK_DEFINITIONS.items()):
		perk_slot: int = 26 - i
		lore_parts: list[str] = [
			f'{{"text":"{line}","color":"gray","italic":false}}'
			for line in PERK_DESCRIPTIONS.get(pid, [])
		]
		lore_parts.append('{"text":"Owned perk","color":"dark_gray","italic":false}')
		lore_snbt: str = "[" + ",".join(lore_parts) + "]"
		perk_item: str = (
			f'minecraft:paper[item_model="{ns}:perk_machine_{pid}",'
			f"custom_data={{{ns}:{{zb_perk_display:true}}}},"
			f'item_name={{"text":"{pdata.display_name}","color":"{pdata.text_color}","italic":false}},'
			f"lore={lore_snbt}]"
		)
		# Owned but not yet shown -> place it once. Not owned but a stale display is here -> clear it.
		perk_display_lines.append(
			f"execute if score @s {ns}.zb.perk.{pid} matches 1 unless items entity @s inventory.{perk_slot} "
			f"*[custom_data~{{{ns}:{{zb_perk_display:true}}}}] run item replace entity @s inventory.{perk_slot} with {perk_item}"
		)
		perk_display_lines.append(
			f"execute unless score @s {ns}.zb.perk.{pid} matches 1 if items entity @s inventory.{perk_slot} "
			f"*[custom_data~{{{ns}:{{zb_perk_display:true}}}}] run item replace entity @s inventory.{perk_slot} with air"
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

