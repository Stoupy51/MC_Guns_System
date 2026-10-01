""" Browsing your own loadouts and the manage dialog behind each row. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.catalogs import (
	PICK10_TOTAL,
	TRIG_DELETE_BASE,
	TRIG_EDIT_BASE,
	TRIG_EDITOR_START,
	TRIG_MANAGE_BASE,
	TRIG_MY_LOADOUTS,
	TRIG_MY_LOADOUTS_FAV_ONLY,
	TRIG_SELECT_BASE,
	TRIG_SET_DEFAULT_BASE,
	TRIG_TOGGLE_VIS_BASE,
)
from ....helpers.text import Text
from .shared import PERK_CONCAT, compute_trig, normalize_btn_fields


# Functions
def write_my_loadouts() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## The player's own loadouts: a Favorites, All and Create filter row, then favorites, then private, then public ones.

	def my_loadouts_dialog_init() -> str:
		"""SNBT for the base My Loadouts dialog (no actions yet)."""
		return (
			f'{{type:"minecraft:multi_action",'
			f'title:{{text:"My Loadouts",color:"gold",bold:true}},'
			f'body:{{type:"minecraft:item",item:{{id:"minecraft:written_book"}},description:{{contents:{{text:"Click a loadout to manage it",color:"gray"}}}},show_decoration:false,show_tooltip:true}},'
			f'actions:[],'
			f'columns:3,'
			f'after_action:"close",'
			f'exit_action:{{label:"Back",action:{{type:"run_command",command:"/trigger {ns}.player.config set 4"}}}}'
			f'}}'
		)

	def my_loadouts_filter_btns(active: str = "all") -> list[str]:
		""" Return the 3 filter button SNBT entries for My Loadouts """
		fav_color = "gold" if active == "fav" else "yellow"
		all_color = "aqua" if active == "all" else "white"
		return [
			f'{{label:{Text.styled_text("\u2b50 Favorites", color=fav_color, bold="true")},tooltip:{{text:"Show only your favorited loadouts"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MY_LOADOUTS_FAV_ONLY}"}}}}',
			f'{{label:{Text.styled_text("\U0001f4cb All", color=all_color, bold="true")},tooltip:{{text:"Show all your loadouts (favorites first, then private, then public)"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MY_LOADOUTS}"}}}}',
			f'{{label:{Text.styled_text("\u271a Create", color="green", bold="true")},tooltip:{{text:"Build a new custom loadout from scratch"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_EDITOR_START}"}}}}',
		]

	## Three passes (favorites, private, public) under the filter row.
	write_versioned_function("multiplayer/my_loadouts/browse", f"""
data modify storage {ns}:temp dialog set value {my_loadouts_dialog_init()}

data modify storage {ns}:temp dialog.actions append value {my_loadouts_filter_btns("all")[0]}
data modify storage {ns}:temp dialog.actions append value {my_loadouts_filter_btns("all")[1]}
data modify storage {ns}:temp dialog.actions append value {my_loadouts_filter_btns("all")[2]}

# Read for the ordering.
function {ns}:v{version}/multiplayer/shared/load_player_favorites

data modify storage {ns}:temp _iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/build_list_favs

data modify storage {ns}:temp _iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/build_list_privates

data modify storage {ns}:temp _iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/build_list_publics

function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## Only the player's favorited loadouts.
	write_versioned_function("multiplayer/my_loadouts/browse_fav_only", f"""
data modify storage {ns}:temp dialog set value {my_loadouts_dialog_init()}
data modify storage {ns}:temp dialog.title set value [{{text:"",color:"gold",bold:true}},{{text:"My Loadouts"}}," \u2014 ",{{text:"Favorites"}}]

data modify storage {ns}:temp dialog.actions append value {my_loadouts_filter_btns("fav")[0]}
data modify storage {ns}:temp dialog.actions append value {my_loadouts_filter_btns("fav")[1]}
data modify storage {ns}:temp dialog.actions append value {my_loadouts_filter_btns("fav")[2]}

function {ns}:v{version}/multiplayer/shared/load_player_favorites

data modify storage {ns}:temp _iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/build_list_favs

function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	write_versioned_function("multiplayer/my_loadouts/build_list_favs", f"""
execute store result score #entry_owner {ns}.data run data get storage {ns}:temp _iter[0].owner_pid
execute if score #entry_owner {ns}.data = @s {ns}.mp.pid run function {ns}:v{version}/multiplayer/shared/check_is_fav
execute if score #entry_owner {ns}.data = @s {ns}.mp.pid if score #is_fav {ns}.data matches 1 run function {ns}:v{version}/multiplayer/my_loadouts/prep_btn

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/build_list_favs
""")

	write_versioned_function("multiplayer/my_loadouts/build_list_privates", f"""
execute store result score #entry_owner {ns}.data run data get storage {ns}:temp _iter[0].owner_pid
execute if score #entry_owner {ns}.data = @s {ns}.mp.pid run function {ns}:v{version}/multiplayer/my_loadouts/check_private_not_fav

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/build_list_privates
""")

	## Only private loadouts outside the favorites.
	write_versioned_function("multiplayer/my_loadouts/check_private_not_fav", f"""
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 0 run function {ns}:v{version}/multiplayer/shared/check_is_fav
execute if score #pub {ns}.data matches 0 if score #is_fav {ns}.data matches 0 run function {ns}:v{version}/multiplayer/my_loadouts/prep_btn
""")

	write_versioned_function("multiplayer/my_loadouts/build_list_publics", f"""
execute store result score #entry_owner {ns}.data run data get storage {ns}:temp _iter[0].owner_pid
execute if score #entry_owner {ns}.data = @s {ns}.mp.pid run function {ns}:v{version}/multiplayer/my_loadouts/check_public_not_fav

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/build_list_publics
""")

	## Only public loadouts outside the favorites.
	write_versioned_function("multiplayer/my_loadouts/check_public_not_fav", f"""
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 1 run function {ns}:v{version}/multiplayer/shared/check_is_fav
execute if score #pub {ns}.data matches 1 if score #is_fav {ns}.data matches 0 run function {ns}:v{version}/multiplayer/my_loadouts/prep_btn
""")

	# Shared by the list tooltip and the manage dialog body.
	def ml_info(public_label: str) -> str:
		return (
			'["",{"text":"$(main_gun_display)","color":"green"},'
			'{"text":" x$(primary_mag_count) mags","color":"dark_green"},'
			'"\\n",'
			'{"text":"$(secondary_gun_display)","color":"yellow"},'
			'{"text":" x$(secondary_mag_count) mags","color":"gold"},'
			'"\\n",'
			'[{"text":"","color":"gray"},{"text":"Grenades"},": "],'
			'{"text":"$(equip_slot1_name)","color":"aqua"},'
			'{"text":" + $(equip_slot2_name)","color":"aqua"},'
			'"\\n",'
			'[{"text":"","color":"white"},{"text":"Points"},": "],'
			f'{{"text":"$(points_used)/{PICK10_TOTAL}pts","color":"gold"}},'
			'[{"text":"","color":"white"},"  ",{"text":"Perks"},": "],'
			'{"text":"$(perks_count)","color":"light_purple"},'
			'{"text":"' + PERK_CONCAT + '","color":"light_purple"},'
			'"\\n",'
			'{"text":"\\u2665 $(likes) likes","color":"red"},'
			'{"text":"  \\u2b50 $(favorites_count) favs","color":"yellow"},'
			'"\\n",'
			+ public_label
			+ ']'
		)

	ml_tooltip_pub = ml_info('{"text":"Public","color":"green","italic":true},"\\n\\n",{"text":"\\u25b6 Click to manage","color":"dark_gray","italic":true}')
	ml_tooltip_priv = ml_info('{"text":"Private","color":"red","italic":true},"\\n\\n",{"text":"\\u25b6 Click to manage","color":"dark_gray","italic":true}')

	## Each loadout is one row opening its manage submenu.
	write_versioned_function("multiplayer/my_loadouts/prep_btn", f"""
data modify storage {ns}:temp _btn_data set from storage {ns}:temp _iter[0]

# TRIG_MANAGE_BASE + id.
{compute_trig(ns, "manage_trig", TRIG_MANAGE_BASE)}

{normalize_btn_fields(ns)}

# Green for public, red for private.
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 1 run function {ns}:v{version}/multiplayer/my_loadouts/add_btn_public with storage {ns}:temp _btn_data
execute if score #pub {ns}.data matches 0 run function {ns}:v{version}/multiplayer/my_loadouts/add_btn_private with storage {ns}:temp _btn_data
""")

	## One row: the name and an arrow, opening the manage submenu.
	write_versioned_function("multiplayer/my_loadouts/add_btn_public", f"""$data modify storage {ns}:temp dialog.actions append value {{label:["",{{"text":"$(name)",color:"green"}},{{"text":"  \\u25b6","color":"dark_gray"}}],tooltip:{ml_tooltip_pub},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(manage_trig)"}}}}
""")
	write_versioned_function("multiplayer/my_loadouts/add_btn_private", f"""$data modify storage {ns}:temp dialog.actions append value {{label:["",{{"text":"$(name)",color:"red"}},{{"text":"  \\u25b6","color":"dark_gray"}}],tooltip:{ml_tooltip_priv},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(manage_trig)"}}}}
""")

	## Per-loadout manage submenu: Use, Edit, Visibility, Default, Delete.
	def compute_trig_id(field: str, base: int) -> str:
		"""Compute base + #loadout_id into _btn_data.<field> (manage submenu)."""
		return (
			f"scoreboard players operation #trig {ns}.data = #loadout_id {ns}.data\n"
			f"scoreboard players add #trig {ns}.data {base}\n"
			f"execute store result storage {ns}:temp _btn_data.{field} int 1 run scoreboard players get #trig {ns}.data"
		)

	write_versioned_function("multiplayer/my_loadouts/manage", f"""
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_MANAGE_BASE}
data modify storage {ns}:temp _find_iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _find_iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/manage_find
""")

	## By id and ownership.
	write_versioned_function("multiplayer/my_loadouts/manage_find", f"""
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _find_iter[0].id
execute store result score #entry_owner {ns}.data run data get storage {ns}:temp _find_iter[0].owner_pid
execute if score #entry_id {ns}.data = #loadout_id {ns}.data if score #entry_owner {ns}.data = @s {ns}.mp.pid run return run function {ns}:v{version}/multiplayer/my_loadouts/manage_prep
data remove storage {ns}:temp _find_iter[0]
execute if data storage {ns}:temp _find_iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/manage_find
""")

	write_versioned_function("multiplayer/my_loadouts/manage_prep", f"""
data modify storage {ns}:temp _btn_data set from storage {ns}:temp _find_iter[0]
{compute_trig_id("select_trig", TRIG_SELECT_BASE)}
{compute_trig_id("edit_trig", TRIG_EDIT_BASE)}
{compute_trig_id("vis_trig", TRIG_TOGGLE_VIS_BASE)}
{compute_trig_id("delete_trig", TRIG_DELETE_BASE)}
{compute_trig_id("default_trig", TRIG_SET_DEFAULT_BASE)}
{normalize_btn_fields(ns)}
execute store result score #pub {ns}.data run data get storage {ns}:temp _find_iter[0].public
execute if score #pub {ns}.data matches 1 run function {ns}:v{version}/multiplayer/my_loadouts/manage_build_public with storage {ns}:temp _btn_data
execute if score #pub {ns}.data matches 0 run function {ns}:v{version}/multiplayer/my_loadouts/manage_build_private with storage {ns}:temp _btn_data
""")

	# Without the "click to manage" hint.
	manage_body_pub = ml_info('{"text":"Public","color":"green","italic":true}')
	manage_body_priv = ml_info('{"text":"Private","color":"red","italic":true}')

	def manage_dialog(vis_label: str, vis_tip: str, vis_color: str) -> str:
		""" Shared manage dialog: Use / Edit / Toggle visibility / Set default / Delete + Back """
		return (
			'{type:"minecraft:multi_action",'
			'title:{text:"$(name)",color:"gold",bold:true},'
			'body:[{type:"minecraft:plain_message",contents:BODY}],'
			'actions:['
			f'{{label:{Text.styled_text("▶ Use this loadout", color="green", bold="true")},tooltip:{{text:"Equip this loadout (applies on next spawn)"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(select_trig)"}}}},'
			f'{{label:{Text.styled_text("✏ Edit", color="gold")},tooltip:{{text:"Re-open the loadout editor pre-filled; saving overwrites this loadout",color:"yellow"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(edit_trig)"}}}},'
			f'{{label:{{text:"{vis_label}",color:"{vis_color}"}},tooltip:{{text:"{vis_tip}"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(vis_trig)"}}}},'
			f'{{label:{Text.styled_text("⭐ Set as Default", color="yellow")},tooltip:{{text:"Auto-equip this loadout when a game starts"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(default_trig)"}}}},'
			f'{{label:{Text.styled_text("\U0001f5d1 Delete", color="red")},tooltip:{{text:"Permanently delete this loadout",color:"dark_red"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(delete_trig)"}}}}'
			'],'
			'columns:1,'
			'after_action:"close",'
			f'exit_action:{{label:"Back",action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MY_LOADOUTS}"}}}}'
			'}'
		)

	write_versioned_function("multiplayer/my_loadouts/manage_build_public", f"""$data modify storage {ns}:temp dialog set value {manage_dialog("Public -> Private", "Toggle this loadout to Private", "dark_aqua").replace("BODY", manage_body_pub)}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")
	write_versioned_function("multiplayer/my_loadouts/manage_build_private", f"""$data modify storage {ns}:temp dialog set value {manage_dialog("Private -> Public", "Toggle this loadout to Public", "aqua").replace("BODY", manage_body_priv)}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

