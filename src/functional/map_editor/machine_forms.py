""" Dialog forms of the zombies machines: what a wallbuy sells and with which ammo, the perk a machine gives, and a trap's settings. """
# Imports
import json
from dataclasses import dataclass

from stewbeet import JsonDict, Mem, write_versioned_function

from ...config.catalogs import GRENADE_TYPES, PRIMARY_WEAPONS, SECONDARY_WEAPONS
from ...config.stats.keys import CAPACITY, COOLDOWN, DAMAGE, PELLET_COUNT, RELOAD_TIME, SINGLE_RELOAD
from ...config.stats.weapons.grenades import LETHAL_GRENADE_IDS, TACTICAL_GRENADE_IDS
from ...config.stats.weapons.melee import MELEE_WEAPONS
from ...database.items import WEAPON_STATS
from ..helpers import MGS_TAG
from ..helpers.text import Text
from ..zombies.machines.perks.definitions import PERK_DEFINITIONS, PERK_DESCRIPTIONS, RECOMMENDED_PRICES
from .shared import doc_hover, help_legend


# Classes
@dataclass(frozen=True)
class WallbuyItem:
	""" One item a wallbuy can sell. """
	item_id: str
	display_name: str
	category: str
	magazine_id: str = ""
	""" The ammo it comes with, empty for a knife or a grenade. """
	stats: str = ""
	""" One line of numbers for the tooltip of its button. """


# Constants
GRENADE_NAMES: dict[str, str] = {**{grenade.item_id: grenade.display_name for grenade in GRENADE_TYPES}, "monkey_bomb": "Monkey Bomb"}
TRAP_TYPES: tuple[str, ...] = ("Fire", "Electric", "Turret")
""" Trap `type` 0, 1 and 2. """


# Functions
def gun_stats(item_id: str) -> str:
	""" The damage, capacity, fire rate and reload of a gun, as its wallbuy button's tooltip shows them.

	>>> gun_stats("ak47")
	'Damage 15 · Capacity 30 · 600 RPM · Reload 3.5 s'
	>>> gun_stats("spas12")
	'Damage 13 x3 pellets · Capacity 8 · 75 RPM · Reload 1.0 s per shell'
	>>> gun_stats("m1911")
	'Damage 11 · Capacity 7 · as fast as clicked · Reload 2.2 s'
	"""
	stats: JsonDict = WEAPON_STATS[item_id]["stats"]
	pellets: str = f"{stats[DAMAGE]} x{stats[PELLET_COUNT]} pellets" if PELLET_COUNT in stats else f"{stats[DAMAGE]}"
	rate: str = f"{1200 // stats[COOLDOWN]} RPM" if stats.get(COOLDOWN) else "as fast as clicked"
	reload: str = f"Reload {stats[RELOAD_TIME] / 20:.1f} s" + (" per shell" if stats.get(SINGLE_RELOAD) else "")
	return f"Damage {pellets} · Capacity {stats[CAPACITY]} · {rate} · {reload}"


def wallbuy_items() -> list[WallbuyItem]:
	""" Every item a wallbuy can sell: guns with their magazine, knives, lethal and tactical grenades. """
	return [
		*(WallbuyItem(item_id=w.item_id, display_name=w.display_name, category=w.category, magazine_id=w.magazine_id,
			stats=gun_stats(w.item_id) if w.item_id in WEAPON_STATS else "") for w in PRIMARY_WEAPONS),
		*(WallbuyItem(item_id=w.item_id, display_name=w.display_name, category="Pistol", magazine_id=w.magazine_id,
			stats=gun_stats(w.item_id)) for w in SECONDARY_WEAPONS),
		*(WallbuyItem(item_id=m.item_id, display_name=m.display_name, category="Knife", stats=f"Damage {m.bo_damage}") for m in MELEE_WEAPONS),
		*(WallbuyItem(item_id=g, display_name=GRENADE_NAMES[g], category="Lethal grenade") for g in LETHAL_GRENADE_IDS),
		*(WallbuyItem(item_id=g, display_name=GRENADE_NAMES[g], category="Tactical grenade") for g in TACTICAL_GRENADE_IDS),
	]


def write_machine_forms(form: str, show_dialog: str, target: str, gone: str) -> None:
	ns: str = Mem.ctx.project_id
	write_wallbuy_form(ns, form, show_dialog, target, gone)
	write_perk_form(ns, form, show_dialog, target, gone)
	write_trap_form(ns, form, show_dialog, target, gone)


def text_input(key: str, label: str, doc: tuple[str, str] | str | None = None, width: int = 200) -> JsonDict:
	""" A one-line text input, its label showing a FIELD_DOCS entry on hover when given one. """
	return {"type": "minecraft:text", "key": key, "label": {"text": label, "hover_event": doc_hover(doc)} if doc else label, "initial": "", "max_length": 64, "width": width}


def write_wallbuy_form(ns: str, form: str, show_dialog: str, target: str, gone: str) -> None:
	""" Write the wallbuy form: its prices and name, an ammo choice, and one button per item, which saves the form with that item. """
	items: list[WallbuyItem] = wallbuy_items()
	magazines: list[WallbuyItem] = [item for item in items if item.magazine_id]
	fields: str = 'name:"$(name)",price:$(price),refill_price:$(refill_price),refill_price_pap:$(refill_price_pap),magazine:"$(magazine)"'

	def item_button(item: WallbuyItem) -> JsonDict:
		ammo: str = f"With {item.magazine_id}" if item.magazine_id else "No ammo"
		tooltip: str = "\n".join(line for line in (item.category, ammo, item.stats) if line)
		return {"label": item.display_name, "tooltip": {"text": tooltip}, "width": 100, "action": {
			"type": "dynamic/run_command", "template": f'/function {form}/wallbuy_apply {{{fields},weapon:"{item.item_id}",own_magazine:"{item.magazine_id}"}}',
		}}

	dialog: JsonDict = {
		"type": "minecraft:multi_action",
		"title": {"text": "Wallbuy", "color": "yellow", "bold": True},
		"body": [
			{"type": "minecraft:plain_message", "width": 400, "contents": ["", {"text": "Sells ", "color": "gray"}, {"text": "", "color": "yellow"},
				{"text": " with ", "color": "gray"}, {"text": "", "color": "yellow"}]},
			{"type": "minecraft:plain_message", "width": 400, "contents": Text.help(
				"Click an item to sell it, with the fields below.\n`Its own` ammo is the item's magazine, or the current one on Save.\nHover an item for its ammo and stats."
			)},
		],
		"inputs": [
			text_input("name", "Name (empty: the item's)"),
			text_input("price", "Price", "price"),
			text_input("refill_price", "Ammo refill price"),
			text_input("refill_price_pap", "Ammo refill price, Pack-a-Punched"),
			{"type": "minecraft:single_option", "key": "magazine", "label": "Ammo", "width": 300, "options": [
				{"id": "auto", "display": "Its own", "initial": True},
				{"id": "none", "display": "None"},
				*({"id": item.magazine_id, "display": f"{item.magazine_id} ({item.display_name})"} for item in magazines),
			]},
		],
		"actions": [
			{"label": {"text": "Save", "color": "green"}, "tooltip": {"text": "Keeps the item it sells"}, "width": 100, "action": {
				"type": "dynamic/run_command", "template": f'/function {form}/wallbuy_apply {{{fields},weapon:"",own_magazine:""}}',
			}},
			*(item_button(item) for item in items),
		],
		"columns": 4,
		"exit_action": {"label": {"text": "Cancel", "color": "gray"}},
	}
	write_versioned_function("maps/editor/form/open/wallbuy", f"""
function {form}/target
data modify storage {ns}:temp dialog set value {json.dumps(dialog, ensure_ascii=False)}
data modify storage {ns}:temp dialog.body[0].contents[2].text set from entity @s data.weapon_id
data modify storage {ns}:temp dialog.body[0].contents[4].text set from entity @s data.magazine_id
execute if data entity @s data{{magazine_id:""}} run data modify storage {ns}:temp dialog.body[0].contents[4].text set value "no ammo"
data modify storage {ns}:temp dialog.inputs[0].initial set from entity @s data.title
data modify storage {ns}:temp dialog.inputs[1].initial set string entity @s data.price
data modify storage {ns}:temp dialog.inputs[2].initial set string entity @s data.refill_price
data modify storage {ns}:temp dialog.inputs[3].initial set string entity @s data.refill_price_pap
{show_dialog}
""")

	## Run as the editor. An empty weapon keeps the one sold; "auto" ammo is then the clicked item's own, or the current one.
	write_versioned_function("maps/editor/form/wallbuy_apply", f"""
execute unless entity {target} run return run {gone}
$data modify storage {ns}:temp _form set value {{title:"$(name)",price:$(price),refill_price:$(refill_price),refill_price_pap:$(refill_price_pap)}}
$data modify storage {ns}:temp _form_pick set value {{weapon:"$(weapon)",own:"$(own_magazine)",magazine:"$(magazine)"}}
execute unless data storage {ns}:temp _form_pick{{weapon:""}} run data modify storage {ns}:temp _form.weapon_id set from storage {ns}:temp _form_pick.weapon
execute unless data storage {ns}:temp _form_pick{{weapon:""}} if data storage {ns}:temp _form_pick{{magazine:"auto"}} run data modify storage {ns}:temp _form.magazine_id set from storage {ns}:temp _form_pick.own
execute if data storage {ns}:temp _form_pick{{magazine:"none"}} run data modify storage {ns}:temp _form.magazine_id set value ""
execute unless data storage {ns}:temp _form_pick{{magazine:"auto"}} unless data storage {ns}:temp _form_pick{{magazine:"none"}} run data modify storage {ns}:temp _form.magazine_id set from storage {ns}:temp _form_pick.magazine
execute as {target} run data modify entity @s data merge from storage {ns}:temp _form
tellraw @s [{MGS_TAG},{{"text":"Wallbuy saved: ","color":"green"}},{{"entity":"{target}","nbt":"data.weapon_id","color":"yellow"}},{{"text":" with ","color":"green"}},{{"entity":"{target}","nbt":"data.magazine_id","color":"yellow"}}]
""")


def write_perk_form(ns: str, form: str, show_dialog: str, target: str, gone: str) -> None:
	""" Write the perk machine form: its price, chip-in, name and power, and one button per perk, which saves the form with that perk. """
	fields: str = 'name:"$(name)",price:$(price),partial_price:$(partial_price),power:$(power)'
	dialog: JsonDict = {
		"type": "minecraft:multi_action",
		"title": {"text": "Perk Machine", "color": "dark_purple", "bold": True},
		"body": [
			{"type": "minecraft:plain_message", "width": 400, "contents": ["", {"text": "Gives ", "color": "gray"}, {"text": "", "color": "light_purple"}]},
			{"type": "minecraft:plain_message", "width": 400, "contents": Text.help("Click a perk to give it, with the fields below. Hover a perk for what it does.")},
		],
		"inputs": [
			text_input("name", "Name (empty: the perk's)", ("perk_machine", "name")),
			text_input("price", "Price (-1: the recommended one)", ("perk_machine", "price")),
			text_input("partial_price", "Chip-in payment (0: off)", ("perk_machine", "partial_price")),
			{"type": "minecraft:boolean", "key": "power", "label": "Only once the power is on", "initial": True, "on_true": "1", "on_false": "0"},
		],
		"actions": [
			{"label": {"text": "Save", "color": "green"}, "tooltip": {"text": "Keeps the perk it gives"}, "width": 100,
				"action": {"type": "dynamic/run_command", "template": f'/function {form}/perk_apply {{{fields},perk:""}}'}},
			*({"label": {"text": perk.display_name, "color": perk.text_color}, "width": 100,
				"tooltip": {"text": "\n".join([*PERK_DESCRIPTIONS.get(perk_id, []), f"Recommended price: {RECOMMENDED_PRICES.get(perk_id, 2000)}"])},
				"action": {"type": "dynamic/run_command", "template": f'/function {form}/perk_apply {{{fields},perk:"{perk_id}"}}'}}
				for perk_id, perk in PERK_DEFINITIONS.items()),
		],
		"columns": 4,
		"exit_action": {"label": {"text": "Cancel", "color": "gray"}},
	}
	write_versioned_function("maps/editor/form/open/perk_machine", f"""
function {form}/target
data modify storage {ns}:temp dialog set value {json.dumps(dialog, ensure_ascii=False)}
data modify storage {ns}:temp dialog.body[0].contents[2].text set from entity @s data.perk_id
data modify storage {ns}:temp dialog.inputs[0].initial set from entity @s data.title
data modify storage {ns}:temp dialog.inputs[1].initial set string entity @s data.price
data modify storage {ns}:temp dialog.inputs[2].initial set string entity @s data.partial_price
data modify storage {ns}:temp dialog.inputs[3].initial set from entity @s data.power
{show_dialog}
""")

	## Run as the editor. An empty perk keeps the one given.
	write_versioned_function("maps/editor/form/perk_apply", f"""
execute unless entity {target} run return run {gone}
$data modify storage {ns}:temp _form set value {{title:"$(name)",price:$(price),partial_price:$(partial_price),power:$(power)b}}
$data modify storage {ns}:temp _form.perk_id set value "$(perk)"
execute if data storage {ns}:temp _form{{perk_id:""}} run data remove storage {ns}:temp _form.perk_id
execute as {target} run data modify entity @s data merge from storage {ns}:temp _form
tellraw @s [{MGS_TAG},{{"text":"Perk machine saved: ","color":"green"}},{{"entity":"{target}","nbt":"data.perk_id","color":"light_purple"}}]
""")


def write_trap_form(ns: str, form: str, show_dialog: str, target: str, gone: str) -> None:
	""" Write the trap form: its type, price, timings, power, effect radius and offset. """
	dialog: JsonDict = {
		"type": "minecraft:multi_action",
		"title": {"text": "Trap", "color": "red", "bold": True},
		"body": [help_legend([("Type", ("trap", "type")), ("Duration", ("trap", "duration")), ("Cooldown", ("trap", "cooldown")), ("Power", "power")])],
		"inputs": [
			{"type": "minecraft:single_option", "key": "type", "label": "Type", "width": 300,
				"options": [{"id": str(index), "display": name} for index, name in enumerate(TRAP_TYPES)]},
			text_input("price", "Price", "price"),
			text_input("duration", "Duration, in ticks", ("trap", "duration")),
			text_input("cooldown", "Cooldown, in ticks", ("trap", "cooldown")),
			{"type": "minecraft:boolean", "key": "power", "label": "Only once the power is on", "initial": True, "on_true": "1", "on_false": "0"},
			text_input("effect_radius", "Effect radius: x, y, z", width=300),
			text_input("offset_pos", "Effect centre from the trap: x, y, z", width=300),
		],
		"actions": [{"label": {"text": "Save", "color": "green"}, "action": {"type": "dynamic/run_command", "template": (
			f'/function {form}/trap_apply {{type:$(type),price:$(price),duration:$(duration),cooldown:$(cooldown),power:$(power),'
			'effect_radius:"$(effect_radius)",offset_pos:"$(offset_pos)"}'
		)}}],
		"exit_action": {"label": {"text": "Cancel", "color": "gray"}},
	}
	types: str = "\n".join(
		f"execute if data entity @s data{{type:{index}}} run data modify storage {ns}:temp dialog.inputs[0].options[{index}].initial set value 1b"
		for index in range(len(TRAP_TYPES))
	)
	write_versioned_function("maps/editor/form/open/trap", f"""
function {form}/target
data modify storage {ns}:temp dialog set value {json.dumps(dialog, ensure_ascii=False)}
{types}
data modify storage {ns}:temp dialog.inputs[1].initial set string entity @s data.price
data modify storage {ns}:temp dialog.inputs[2].initial set string entity @s data.duration
data modify storage {ns}:temp dialog.inputs[3].initial set string entity @s data.cooldown
data modify storage {ns}:temp dialog.inputs[4].initial set from entity @s data.power

# The lists without their brackets.
function {form}/open/trap_texts with entity @s data
{show_dialog}
""")
	write_versioned_function("maps/editor/form/open/trap_texts", f"""
$data modify storage {ns}:temp _form_text set value '$(effect_radius)'
data modify storage {ns}:temp dialog.inputs[5].initial set string storage {ns}:temp _form_text 1 -1
$data modify storage {ns}:temp _form_text set value '$(offset_pos)'
data modify storage {ns}:temp dialog.inputs[6].initial set string storage {ns}:temp _form_text 1 -1
""")

	# The radius is a list of floats whatever was typed, as the editor places it.
	radius_floats: str = "\n".join(
		f"execute store result storage {ns}:temp _form.effect_radius[{index}] float 0.01 run data get storage {ns}:temp _form.effect_radius[{index}] 100"
		for index in range(3)
	)
	## Run as the editor.
	write_versioned_function("maps/editor/form/trap_apply", f"""
execute unless entity {target} run return run {gone}
$data modify storage {ns}:temp _form set value {{type:$(type),price:$(price),duration:$(duration),cooldown:$(cooldown),power:$(power)b,effect_radius:[$(effect_radius)],offset_pos:[$(offset_pos)]}}
{radius_floats}
execute as {target} run data modify entity @s data merge from storage {ns}:temp _form
tellraw @s [{MGS_TAG},{{"text":"Trap saved.","color":"green"}}]
""")

