""" The editor hotbar: one spawn egg per element, plus destroy, save, exit and the coord stick. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..map_editor_defs import ALL_ELEMENTS, EDITOR_MODES, MODE_LIST


# Functions
def write_editor_tools() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Give Editor Tools (dispatch by mode score).
	destroy_cmd = (
		f'item replace entity @s hotbar.8 with minecraft:bat_spawn_egg'
		f'[minecraft:item_name={{"text":"✘ DESTROY","color":"dark_red","italic":false,"bold":true}},'
		f'minecraft:item_model="minecraft:wither_skeleton_spawn_egg",'
		f'minecraft:custom_data={{{ns}:{{editor:true,type:"destroy"}}}},'
		f'minecraft:entity_data={{id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["{ns}.new_element","{ns}.element.destroy"]}}]'
	)

	give_dispatch = "\n".join(
		f'execute if score @s {ns}.mp.map_disp matches {i} run function {ns}:v{version}/maps/editor/give_tools/{mk}'
		for i, mk in enumerate(MODE_LIST)
	)

	save_exit_cmd = (
		f'item replace entity @s inventory.26 with minecraft:bat_spawn_egg'
		f'[minecraft:item_name=["","💾 ",{{"text":"Save & Exit","color":"green","italic":false,"bold":true}}],'
		f'minecraft:item_model="minecraft:turtle_spawn_egg",'
		f'minecraft:custom_data={{{ns}:{{editor:true,type:"editor_save_exit"}}}},'
		f'minecraft:entity_data={{id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["{ns}.new_element","{ns}.element.editor_save_exit"]}}]'
	)

	exit_cmd = (
		f'item replace entity @s inventory.25 with minecraft:bat_spawn_egg'
		f'[minecraft:item_name={{"text":"✘ Exit","color":"red","italic":false,"bold":true}},'
		f'minecraft:item_model="minecraft:ghast_spawn_egg",'
		f'minecraft:custom_data={{{ns}:{{editor:true,type:"editor_exit"}}}},'
		f'minecraft:entity_data={{id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["{ns}.new_element","{ns}.element.editor_exit"]}}]'
	)

	save_only_cmd = (
		f'item replace entity @s inventory.24 with minecraft:bat_spawn_egg'
		f'[minecraft:item_name=["","💾 ",{{"text":"Save","color":"aqua","italic":false,"bold":true}}],'
		f'minecraft:item_model="minecraft:axolotl_spawn_egg",'
		f'minecraft:custom_data={{{ns}:{{editor:true,type:"editor_save"}}}},'
		f'minecraft:entity_data={{id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["{ns}.new_element","{ns}.element.editor_save"]}}]'
	)

	coord_stick_cmd = (
		f'item replace entity @s inventory.23 with minecraft:warped_fungus_on_a_stick'
		f'[minecraft:item_name=["","📐 ",{{"text":"Coord Stick","color":"yellow","italic":false,"bold":true}}],'
		f'minecraft:custom_data={{{ns}:{{coord_stick:true}}}},'
		f'minecraft:item_model="minecraft:stick",'
		f'minecraft:enchantment_glint_override=true]'
	)

	write_versioned_function("maps/editor/give_tools", f"""
# Destroy egg (always in hotbar.8)
{destroy_cmd}

# Utility eggs (bottom-right of inventory)
{save_exit_cmd}
{exit_cmd}
{save_only_cmd}

# Coord stick utility
{coord_stick_cmd}

# Mode-specific eggs
{give_dispatch}
""")

	# Per-mode give_tools
	for mode_key, mode_info in EDITOR_MODES.items():
		egg_cmds: list[str] = []
		for etype, eslot in mode_info.slots.items():
			einfo = ALL_ELEMENTS[etype]
			egg_cmds.append(
				f'item replace entity @s {eslot} with minecraft:bat_spawn_egg'
				f'[minecraft:item_name={{"text":"{einfo.name}","color":"{einfo.color}","italic":false}},'
				f'minecraft:item_model="{einfo.egg_model}",'
				f'minecraft:custom_data={{{ns}:{{editor:true,type:"{etype}"}}}},'
				f'minecraft:entity_data={{id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["{ns}.new_element","{ns}.element.{etype}"]}}]'
			)
		# Zombies mode: add defaults config (hotbar.6) and configure element (hotbar.7) tools
		if mode_key == "zombies":
			egg_cmds.append(
				f'item replace entity @s hotbar.6 with minecraft:bat_spawn_egg'
				f'[minecraft:item_name={{"text":"⚙ Defaults","color":"white","italic":false,"bold":true}},'
				f'minecraft:item_model="minecraft:allay_spawn_egg",'
				f'minecraft:custom_data={{{ns}:{{editor:true,type:"zb_defaults"}}}},'
				f'minecraft:entity_data={{id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["{ns}.new_element","{ns}.element.zb_defaults"]}}]'
			)
			egg_cmds.append(
				f'item replace entity @s hotbar.7 with minecraft:bat_spawn_egg'
				f'[minecraft:item_name=["","🔧 ",{{"text":"Configure","color":"aqua","italic":false,"bold":true}}],'
				f'minecraft:item_model="minecraft:breeze_spawn_egg",'
				f'minecraft:custom_data={{{ns}:{{editor:true,type:"zb_configure"}}}},'
				f'minecraft:entity_data={{id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["{ns}.new_element","{ns}.element.zb_configure"]}}]'
			)
		write_versioned_function(
			f"maps/editor/give_tools/{mode_key}",
			"\n".join(egg_cmds) if egg_cmds else "# No eggs for this mode"
		)

