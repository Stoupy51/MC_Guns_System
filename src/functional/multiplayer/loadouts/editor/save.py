""" Building the loadout entry from the editor state and writing it back to storage. """
# Imports
from collections.abc import Sequence

from stewbeet import Mem, write_load_file, write_versioned_function

from .....config.catalogs import (
	GRENADE_TYPES,
	PICK10_TOTAL,
	PRIMARY_WEAPONS,
	SECONDARY_WEAPONS,
	TRIG_SAVE_PUBLIC,
	SecondaryWeapon,
	Weapon,
)
from .....database.items import CONSUMABLE_MAGAZINES
from ....helpers import MGS_TAG
from .shared import editor_fn


# Functions
def write_editor_save() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	fn: str = editor_fn(ns, version)

	## Build the loadout entry from the editor state through the weapon slot tables generated here.
	secondaries: list[SecondaryWeapon] = [w for w in SECONDARY_WEAPONS if w.in_loadout]
	write_load_file(f"""
# Computed at build time.
data modify storage {ns}:multiplayer primary_slot_table set value [{",".join(slot_table_entry(ns, wp, "hotbar.1") for wp in PRIMARY_WEAPONS)}]
data modify storage {ns}:multiplayer secondary_slot_table set value [{",".join(slot_table_entry(ns, wp, "hotbar.2") for wp in secondaries)}]
""")

	save_primary_dispatch: str = slot_table_lookup(ns, "primary", PRIMARY_WEAPONS, "primary_slot_table")
	# Overkill: the secondary may be a primary, looked up in the primary table.
	save_secondary_dispatch: str = (
		slot_table_lookup(ns, "secondary", secondaries, "secondary_slot_table")
		+ slot_table_lookup(ns, "secondary", PRIMARY_WEAPONS, "primary_slot_table")
	)

	equip_name_dispatch: dict[int, str] = {}
	for slot_num, field in [(1, "equip_slot1"), (2, "equip_slot2")]:
		equip_name_dispatch[slot_num] = "\n".join(
			f'execute if data storage {ns}:temp editor{{{field}:"{g.item_id}"}} run data modify storage {ns}:temp _new_loadout.{field}_name set value "{g.display_name}"'
			for g in GRENADE_TYPES if g.item_id
		)

	write_versioned_function("multiplayer/editor/save", f"""
# The hub grays save out, but triggers can be sent by hand.
execute if data storage {ns}:temp editor{{primary:""}} run tellraw @s [{MGS_TAG},{{"text":"A primary weapon is required to save!","color":"red"}}]
execute if data storage {ns}:temp editor{{primary:""}} run return run function {fn}/hub

# So points_used is accurate.
function {fn}/recompute_points

# Visibility comes from the trigger value.
scoreboard players set #cl_public {ns}.data 0
execute if score @s {ns}.player.config matches {TRIG_SAVE_PUBLIC} run scoreboard players set #cl_public {ns}.data 1

data modify storage {ns}:temp _build set value {{}}

{save_primary_dispatch}
{save_secondary_dispatch}
# The primary table gives hotbar.1; a primary used as secondary goes to hotbar.2.
execute if data storage {ns}:temp _build.secondary_data run data modify storage {ns}:temp _build.secondary_data.gun_slot.slot set value "hotbar.2"

data modify storage {ns}:temp _new_loadout set value {{id:0,owner_pid:0,owner_name:"",name:"",public:0b,likes:0,favorites_count:0,points_used:0,main_gun:"",main_gun_display:"",secondary_gun:"",secondary_gun_display:"None",primary_mag_count:1,secondary_mag_count:0,equip_slot1:"",equip_slot1_name:"None",equip_slot2:"",equip_slot2_name:"None",knife_camo:"",perks:[],slots:[]}}
# New loadouts take the counter, edited ones keep their id.
execute if score @s {ns}.mp.edit_target matches ..0 store result storage {ns}:temp _new_loadout.id int 1 run data get storage {ns}:multiplayer next_loadout_id
execute if score @s {ns}.mp.edit_target matches 1.. store result storage {ns}:temp _new_loadout.id int 1 run scoreboard players get @s {ns}.mp.edit_target

# New loadouts only.
execute if score @s {ns}.mp.edit_target matches ..0 store result score #temp {ns}.data run data get storage {ns}:multiplayer next_loadout_id
execute if score @s {ns}.mp.edit_target matches ..0 run scoreboard players add #temp {ns}.data 1
execute if score @s {ns}.mp.edit_target matches ..0 store result storage {ns}:multiplayer next_loadout_id int 1 run scoreboard players get #temp {ns}.data

execute store result storage {ns}:temp _new_loadout.owner_pid int 1 run scoreboard players get @s {ns}.mp.pid

# The player head loot table gives the username.
tag @s add {ns}.username_getter
execute at @s summon item_display run function {ns}:v{version}/multiplayer/get_username
tag @s remove {ns}.username_getter

# Scope and camo variants.
data modify storage {ns}:temp _new_loadout.main_gun set from storage {ns}:temp editor.primary_full
data modify storage {ns}:temp _new_loadout.secondary_gun set from storage {ns}:temp editor.secondary_full

data modify storage {ns}:temp _new_loadout.primary_mag_count set from storage {ns}:temp editor.primary_mag_count
data modify storage {ns}:temp _new_loadout.secondary_mag_count set from storage {ns}:temp editor.secondary_mag_count
data modify storage {ns}:temp _new_loadout.equip_slot1 set from storage {ns}:temp editor.equip_slot1
data modify storage {ns}:temp _new_loadout.equip_slot2 set from storage {ns}:temp editor.equip_slot2
data modify storage {ns}:temp _new_loadout.knife_camo set from storage {ns}:temp editor.knife_camo
data modify storage {ns}:temp _new_loadout.perks set from storage {ns}:temp editor.perks

# So the loadout can be edited later.
data modify storage {ns}:temp _new_loadout.editor_state set from storage {ns}:temp editor

# PICK10_TOTAL - remaining.
scoreboard players set #pts_used {ns}.data {PICK10_TOTAL}
scoreboard players operation #pts_used {ns}.data -= @s {ns}.mp.edit_points
execute store result storage {ns}:temp _new_loadout.points_used int 1 run scoreboard players get #pts_used {ns}.data

execute if data storage {ns}:temp editor{{equip_slot1:""}} run data modify storage {ns}:temp _new_loadout.equip_slot1_name set value "None"
{equip_name_dispatch[1]}
execute if data storage {ns}:temp editor{{equip_slot2:""}} run data modify storage {ns}:temp _new_loadout.equip_slot2_name set value "None"
{equip_name_dispatch[2]}

execute if score #cl_public {ns}.data matches 1 run data modify storage {ns}:temp _new_loadout.public set value 1b

# Loot entries use the scope and camo variant ids.
function {fn}/fix_primary_loot with storage {ns}:temp editor
execute if data storage {ns}:temp _build.secondary_data run function {fn}/fix_secondary_loot with storage {ns}:temp editor

# Slot list. 1: primary (hotbar.1)
data modify storage {ns}:temp _new_loadout.slots append from storage {ns}:temp _build.primary_data.gun_slot

# 2: secondary (hotbar.2), if any
execute if data storage {ns}:temp _build.secondary_data run data modify storage {ns}:temp _new_loadout.slots append from storage {ns}:temp _build.secondary_data.gun_slot

# 3: equipment (hotbar.8 and hotbar.7)
execute unless data storage {ns}:temp editor{{equip_slot1:""}} run function {fn}/append_equip1 with storage {ns}:temp editor
execute unless data storage {ns}:temp editor{{equip_slot2:""}} run function {fn}/append_equip2 with storage {ns}:temp editor

# 4: primary magazines (inventory from 0)
scoreboard players set #inv_slot {ns}.data 0
data modify storage {ns}:temp _mag_data set from storage {ns}:temp _build.primary_data
execute store result score #pmag_count {ns}.data run data get storage {ns}:temp editor.primary_mag_count
execute if score #pmag_count {ns}.data matches 1.. run function {fn}/append_mag_slots

# 5: secondary magazines (continuing from #inv_slot)
execute if data storage {ns}:temp _build.secondary_data run function {fn}/start_secondary_mags

function {fn}/set_name with storage {ns}:temp editor
function {fn}/set_main_gun_display with storage {ns}:temp editor
data modify storage {ns}:temp _new_loadout.secondary_gun_display set value "None"
execute unless data storage {ns}:temp editor{{secondary:""}} run function {fn}/set_sec_gun_display with storage {ns}:temp editor

# Editing replaces the original entry.
execute if score @s {ns}.mp.edit_target matches ..0 run data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _new_loadout
execute if score @s {ns}.mp.edit_target matches 1.. run function {fn}/save_replace

scoreboard players set @s {ns}.mp.edit_target 0

function {fn}/notify_saved with storage {ns}:temp editor
function {ns}:v{version}/multiplayer/my_loadouts/browse
""")

	## Rebuild the list, replacing the original entry (same id and owner) with _new_loadout and keeping its social stats.
	write_versioned_function("multiplayer/editor/save_replace", f"""
scoreboard players operation #edit_id {ns}.data = @s {ns}.mp.edit_target
data modify storage {ns}:temp _edit_src set from storage {ns}:multiplayer custom_loadouts
data modify storage {ns}:multiplayer custom_loadouts set value []
scoreboard players set #edit_replaced {ns}.data 0
execute if data storage {ns}:temp _edit_src[0] run function {fn}/save_replace_iter

# The original was deleted meanwhile: append as new.
execute if score #edit_replaced {ns}.data matches 0 run data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _new_loadout
""")

	write_versioned_function("multiplayer/editor/save_replace_iter", f"""
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _edit_src[0].id
execute store result score #entry_owner {ns}.data run data get storage {ns}:temp _edit_src[0].owner_pid
scoreboard players set #edit_match {ns}.data 0
execute if score #entry_id {ns}.data = #edit_id {ns}.data if score #entry_owner {ns}.data = @s {ns}.mp.pid run scoreboard players set #edit_match {ns}.data 1

execute if score #edit_match {ns}.data matches 1 if data storage {ns}:temp _edit_src[0].likes run data modify storage {ns}:temp _new_loadout.likes set from storage {ns}:temp _edit_src[0].likes
execute if score #edit_match {ns}.data matches 1 if data storage {ns}:temp _edit_src[0].favorites_count run data modify storage {ns}:temp _new_loadout.favorites_count set from storage {ns}:temp _edit_src[0].favorites_count
execute if score #edit_match {ns}.data matches 1 run data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _new_loadout
execute if score #edit_match {ns}.data matches 1 run scoreboard players set #edit_replaced {ns}.data 1
execute unless score #edit_match {ns}.data matches 1 run data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _edit_src[0]

data remove storage {ns}:temp _edit_src[0]
execute if data storage {ns}:temp _edit_src[0] run function {fn}/save_replace_iter
""")

	## Include the camo suffix.
	write_versioned_function("multiplayer/editor/append_equip1", f"""$data modify storage {ns}:temp _new_loadout.slots append value {{slot:"hotbar.8",loot:"{ns}:i/$(equip_slot1)$(equip_slot1_camo)",count:1,consumable:0b,bullets:0}}
""")
	write_versioned_function("multiplayer/editor/append_equip2", f"""$data modify storage {ns}:temp _new_loadout.slots append value {{slot:"hotbar.7",loot:"{ns}:i/$(equip_slot2)$(equip_slot2_camo)",count:1,consumable:0b,bullets:0}}
""")

	write_versioned_function("multiplayer/editor/append_mag_slots", f"""
# Macro arguments cannot use dot paths.
data modify storage {ns}:temp _mag_id set from storage {ns}:temp _mag_data.mag_id
data modify storage {ns}:temp _mag_bullets set from storage {ns}:temp _mag_data.mag_bullets

# Consumable: one slot carrying count and bullets.
execute if data storage {ns}:temp _mag_data{{mag_consumable:1b}} run function {fn}/append_mag_consumable
execute if data storage {ns}:temp _mag_data{{mag_consumable:1b}} run return 0

# Otherwise one slot per magazine.
execute if score #pmag_count {ns}.data matches 1.. run function {fn}/append_mag_loop
""")

	write_versioned_function("multiplayer/editor/append_mag_consumable", f"""
# Total bullets = capacity x chosen count.
execute store result score #mag_bullets {ns}.data run data get storage {ns}:temp _mag_bullets
scoreboard players operation #mag_bullets {ns}.data *= #pmag_count {ns}.data
execute store result storage {ns}:temp _mag_bullets int 1 run scoreboard players get #mag_bullets {ns}.data
execute store result storage {ns}:temp _inv_n int 1 run scoreboard players get #inv_slot {ns}.data
function {fn}/append_mag_consumable_macro with storage {ns}:temp
scoreboard players add #inv_slot {ns}.data 1
""")

	write_versioned_function("multiplayer/editor/append_mag_consumable_macro", f"""$data modify storage {ns}:temp _new_loadout.slots append value {{slot:"inventory.$(_inv_n)",loot:"{ns}:i/$(_mag_id)",count:1,consumable:1b,bullets:$(_mag_bullets)}}
""")

	write_versioned_function("multiplayer/editor/append_mag_loop", f"""
execute if score #pmag_count {ns}.data matches ..0 run return 0
execute store result storage {ns}:temp _inv_n int 1 run scoreboard players get #inv_slot {ns}.data
function {fn}/append_mag_regular with storage {ns}:temp
scoreboard players add #inv_slot {ns}.data 1
scoreboard players remove #pmag_count {ns}.data 1
return run function {fn}/append_mag_loop
""")

	write_versioned_function("multiplayer/editor/append_mag_regular", f"""$data modify storage {ns}:temp _new_loadout.slots append value {{slot:"inventory.$(_inv_n)",loot:"{ns}:i/$(_mag_id)",count:1,consumable:0b,bullets:0}}
""")

	write_versioned_function("multiplayer/editor/start_secondary_mags", f"""
data modify storage {ns}:temp _mag_data set from storage {ns}:temp _build.secondary_data
execute store result score #pmag_count {ns}.data run data get storage {ns}:temp editor.secondary_mag_count
execute if score #pmag_count {ns}.data matches 1.. run function {fn}/append_mag_slots
""")

	write_versioned_function("multiplayer/editor/fix_primary_loot", f"""$data modify storage {ns}:temp _build.primary_data.gun_slot.loot set value "{ns}:i/$(primary_full)"
""")
	write_versioned_function("multiplayer/editor/fix_secondary_loot", f"""$data modify storage {ns}:temp _build.secondary_data.gun_slot.loot set value "{ns}:i/$(secondary_full)"
""")

	write_versioned_function("multiplayer/editor/set_name", f"""$data modify storage {ns}:temp _new_loadout.name set value "$(primary_name) + $(secondary_name)"\n""")
	write_versioned_function("multiplayer/editor/set_main_gun_display", f"""$data modify storage {ns}:temp _new_loadout.main_gun_display set value "$(primary_name) ($(primary_scope_name), $(primary_camo_name))"\n""")
	write_versioned_function("multiplayer/editor/set_sec_gun_display", f"""$data modify storage {ns}:temp _new_loadout.secondary_gun_display set value "$(secondary_name) ($(secondary_scope_name), $(secondary_camo_name))"\n""")
	write_versioned_function("multiplayer/editor/notify_saved", '$tellraw @s ["",' + MGS_TAG + ',[{"text":"","color":"white"},{"text":"Loadout saved"},": "],{"text":"$(primary_name) + $(secondary_name)","color":"green","bold":true}]')


def slot_table_entry(ns: str, weapon: Weapon | SecondaryWeapon, hotbar: str) -> str:
	""" SNBT row of a slot lookup table: the gun's slot on `hotbar`, and how its magazines are given. """
	consumable: bool = weapon.magazine_id in CONSUMABLE_MAGAZINES
	gun_slot: str = f'{{slot:"{hotbar}",loot:"{ns}:i/{weapon.item_id}",count:1,consumable:0b,bullets:0}}'
	return (
		f'{{id:"{weapon.item_id}",gun_slot:{gun_slot},mag_id:"{weapon.magazine_id}",'
		f'mag_consumable:{"1b" if consumable else "0b"},mag_bullets:{weapon.default_mag_count if consumable else 0}}}'
	)


def slot_table_lookup(ns: str, field: str, weapons: Sequence[Weapon | SecondaryWeapon], table: str) -> str:
	""" One line per weapon copying its `table` row into `_build.<field>_data` when the editor's `field` holds it.

	Args:
		weapons: In the order they sit in `table`.
	"""
	return "".join(
		f'execute if data storage {ns}:temp editor{{{field}:"{weapon.item_id}"}} run '
		f"data modify storage {ns}:temp _build.{field}_data set from storage {ns}:multiplayer {table}[{index}]\n"
		for index, weapon in enumerate(weapons)
	)

