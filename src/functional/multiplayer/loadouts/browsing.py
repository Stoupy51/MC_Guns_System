
# ruff: noqa: E501
# Imports

from ...helpers import styled_text
from .catalogs import (
	PERKS,
	PICK10_TOTAL,
	TRIG_DELETE_BASE,
	TRIG_EDIT_BASE,
	TRIG_EDITOR_START,
	TRIG_FAVORITE_BASE,
	TRIG_LIKE_BASE,
	TRIG_MANAGE_BASE,
	TRIG_MARKETPLACE_ALL,
	TRIG_MARKETPLACE_FAV_ONLY,
	TRIG_MARKETPLACE_LIKES,
	TRIG_MY_LOADOUTS,
	TRIG_MY_LOADOUTS_FAV_ONLY,
	TRIG_SELECT_BASE,
	TRIG_SET_DEFAULT_BASE,
	TRIG_TOGGLE_VIS_BASE,
)
from ...generator import McfunctionGenerator


class BrowsingGenerator(McfunctionGenerator):
    """ Generates the browsing datapack functions. """

    def generate(self) -> None:
    	ns: str = self.ns
    	version: str = self.version

    	## ====================================================================
    	## SHARED HELPERS - player favorites loading & is-fav check
    	## ====================================================================

    	## shared/load_player_favorites - Copy current player's favorites list into _cur_favorites
    	self.func("multiplayer/shared/load_player_favorites", f"""
# Default to empty favorites
data modify storage {ns}:temp _cur_favorites set value []
# Scan player_data for our PID entry and copy its favorites list
data modify storage {ns}:temp _pd_iter set from storage {ns}:multiplayer player_data
execute if data storage {ns}:temp _pd_iter[0] run function {ns}:v{version}/multiplayer/shared/load_fav_iter
""")

    	## shared/load_fav_iter - Recursive: find our entry by PID and copy favorites
    	self.func("multiplayer/shared/load_fav_iter", f"""
execute store result score #pd_pid {ns}.data run data get storage {ns}:temp _pd_iter[0].pid
execute if score #pd_pid {ns}.data = @s {ns}.mp.pid run data modify storage {ns}:temp _cur_favorites set from storage {ns}:temp _pd_iter[0].favorites
data remove storage {ns}:temp _pd_iter[0]
# Stop early once our entry is found
execute unless score #pd_pid {ns}.data = @s {ns}.mp.pid if data storage {ns}:temp _pd_iter[0] run function {ns}:v{version}/multiplayer/shared/load_fav_iter
""")

    	## shared/check_is_fav - Sets #is_fav = 1 if _iter[0].id is in _cur_favorites, else 0
    	self.func("multiplayer/shared/check_is_fav", f"""
execute store result score #check_id {ns}.data run data get storage {ns}:temp _iter[0].id
data modify storage {ns}:temp _fav_check set from storage {ns}:temp _cur_favorites
scoreboard players set #is_fav {ns}.data 0
execute if data storage {ns}:temp _fav_check[0] run function {ns}:v{version}/multiplayer/shared/check_fav_iter
""")

    	## shared/check_fav_iter - Recursive: compare each _fav_check entry against #check_id
    	self.func("multiplayer/shared/check_fav_iter", f"""
execute store result score #fav_entry_id {ns}.data run data get storage {ns}:temp _fav_check[0].id
execute if score #fav_entry_id {ns}.data = #check_id {ns}.data run scoreboard players set #is_fav {ns}.data 1
data remove storage {ns}:temp _fav_check[0]
execute unless score #is_fav {ns}.data matches 1 if data storage {ns}:temp _fav_check[0] run function {ns}:v{version}/multiplayer/shared/check_fav_iter
""")

    	## ====================================================================
    	## MY LOADOUTS - Browse and manage player's own custom loadouts
    	## Organized as: [⭐Favorites Only] [📋All] [✚Create] filter row,
    	##                then favorites, then privates, then publics
    	## ====================================================================

    	def _my_loadouts_dialog_init() -> str:
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

    	def _my_loadouts_filter_btns(active: str = "all") -> list[str]:
    		""" Return the 3 filter button SNBT entries for My Loadouts """
    		fav_color = "gold" if active == "fav" else "yellow"
    		all_color = "aqua" if active == "all" else "white"
    		return [
    			f'{{label:{styled_text("\u2b50 Favorites", color=fav_color, bold="true")},tooltip:{{text:"Show only your favorited loadouts"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MY_LOADOUTS_FAV_ONLY}"}}}}',
    			f'{{label:{styled_text("\U0001f4cb All", color=all_color, bold="true")},tooltip:{{text:"Show all your loadouts (favorites first, then private, then public)"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MY_LOADOUTS}"}}}}',
    			f'{{label:{styled_text("\u271a Create", color="green", bold="true")},tooltip:{{text:"Build a new custom loadout from scratch"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_EDITOR_START}"}}}}',
    		]

    	## my_loadouts/browse - Default: 3-pass build (favorites → privates → publics) + filter row
    	self.func("multiplayer/my_loadouts/browse", f"""
# Initialize dialog
data modify storage {ns}:temp dialog set value {_my_loadouts_dialog_init()}

# Add filter/sort buttons (row 1: favorites / all / create)
data modify storage {ns}:temp dialog.actions append value {_my_loadouts_filter_btns("all")[0]}
data modify storage {ns}:temp dialog.actions append value {_my_loadouts_filter_btns("all")[1]}
data modify storage {ns}:temp dialog.actions append value {_my_loadouts_filter_btns("all")[2]}

# Load player favorites for ordering
function {ns}:v{version}/multiplayer/shared/load_player_favorites

# Pass 1: Own loadouts that are in player's favorites
data modify storage {ns}:temp _iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/build_list_favs

# Pass 2: Own private loadouts NOT in favorites
data modify storage {ns}:temp _iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/build_list_privates

# Pass 3: Own public loadouts NOT in favorites
data modify storage {ns}:temp _iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/build_list_publics

# Show dialog
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

    	## my_loadouts/browse_fav_only - Filter: only own favorited loadouts
    	self.func("multiplayer/my_loadouts/browse_fav_only", f"""
# Initialize dialog
data modify storage {ns}:temp dialog set value {_my_loadouts_dialog_init()}
data modify storage {ns}:temp dialog.title set value [{{text:"",color:"gold",bold:true}},{{text:"My Loadouts"}}," \u2014 ",{{text:"Favorites"}}]

# Add filter/sort buttons (favorites tab active)
data modify storage {ns}:temp dialog.actions append value {_my_loadouts_filter_btns("fav")[0]}
data modify storage {ns}:temp dialog.actions append value {_my_loadouts_filter_btns("fav")[1]}
data modify storage {ns}:temp dialog.actions append value {_my_loadouts_filter_btns("fav")[2]}

# Load player favorites
function {ns}:v{version}/multiplayer/shared/load_player_favorites

# Only show own loadouts that are in favorites
data modify storage {ns}:temp _iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/build_list_favs

# Show dialog
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

    	## my_loadouts/build_list_favs - Pass 1: own loadouts in favorites
    	self.func("multiplayer/my_loadouts/build_list_favs", f"""
execute store result score #entry_owner {ns}.data run data get storage {ns}:temp _iter[0].owner_pid
execute if score #entry_owner {ns}.data = @s {ns}.mp.pid run function {ns}:v{version}/multiplayer/shared/check_is_fav
execute if score #entry_owner {ns}.data = @s {ns}.mp.pid if score #is_fav {ns}.data matches 1 run function {ns}:v{version}/multiplayer/my_loadouts/prep_btn

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/build_list_favs
""")

    	## my_loadouts/build_list_privates - Pass 2: own private loadouts NOT in favorites
    	self.func("multiplayer/my_loadouts/build_list_privates", f"""
execute store result score #entry_owner {ns}.data run data get storage {ns}:temp _iter[0].owner_pid
execute if score #entry_owner {ns}.data = @s {ns}.mp.pid run function {ns}:v{version}/multiplayer/my_loadouts/check_private_not_fav

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/build_list_privates
""")

    	## check_private_not_fav - For own entries: only add if private AND not in favorites
    	self.func("multiplayer/my_loadouts/check_private_not_fav", f"""
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 0 run function {ns}:v{version}/multiplayer/shared/check_is_fav
execute if score #pub {ns}.data matches 0 if score #is_fav {ns}.data matches 0 run function {ns}:v{version}/multiplayer/my_loadouts/prep_btn
""")

    	## my_loadouts/build_list_publics - Pass 3: own public loadouts NOT in favorites
    	self.func("multiplayer/my_loadouts/build_list_publics", f"""
execute store result score #entry_owner {ns}.data run data get storage {ns}:temp _iter[0].owner_pid
execute if score #entry_owner {ns}.data = @s {ns}.mp.pid run function {ns}:v{version}/multiplayer/my_loadouts/check_public_not_fav

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/build_list_publics
""")

    	## check_public_not_fav - For own entries: only add if public AND not in favorites
    	self.func("multiplayer/my_loadouts/check_public_not_fav", f"""
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 1 run function {ns}:v{version}/multiplayer/shared/check_is_fav
execute if score #pub {ns}.data matches 1 if score #is_fav {ns}.data matches 0 run function {ns}:v{version}/multiplayer/my_loadouts/prep_btn
""")

    	# Build perk display lines for tooltips
    	# \\n in SNBT → stored as \n (backslash+n, 2 chars) → when macro-substituted: \n = newline in text component
    	_perk_disp = (
    		"\n".join(f"data modify storage {ns}:temp _btn_data.perk{i} set value \"\"" for i in range(len(PERKS)))
    		+ "\n"
    		+ "\n".join(
    			f'execute if data storage {ns}:temp _btn_data{{perks:["{pid}"]}} run data modify storage {ns}:temp _btn_data.perk{i} set value "\\\\n- {pname}"'
    			for i, (pid, pname, _, _) in enumerate(PERKS)
    		)
    	)
    	# Concatenation of every perk slot (unselected ones are empty) — shows all chosen perks
    	_perk_concat = "".join(f"$(perk{i})" for i in range(len(PERKS)))

    	# Shared: normalize optional fields, compute perks count & display for _btn_data
    	_normalize_fields = "\n".join([
    		f'execute unless data storage {ns}:temp _btn_data.perks run data modify storage {ns}:temp _btn_data.perks set value []',
    		f'execute store result storage {ns}:temp _btn_data.perks_count int 1 run data get storage {ns}:temp _btn_data.perks',
    		_perk_disp,
    		f'execute unless data storage {ns}:temp _btn_data.points_used run data modify storage {ns}:temp _btn_data.points_used set value 0',
    		f'execute unless data storage {ns}:temp _btn_data.favorites_count run data modify storage {ns}:temp _btn_data.favorites_count set value 0',
    		f'execute unless data storage {ns}:temp _btn_data.likes run data modify storage {ns}:temp _btn_data.likes set value 0',
    		f'execute unless data storage {ns}:temp _btn_data.primary_mag_count run data modify storage {ns}:temp _btn_data.primary_mag_count set value 1',
    		f'execute unless data storage {ns}:temp _btn_data.secondary_mag_count run data modify storage {ns}:temp _btn_data.secondary_mag_count set value 0',
    		f'execute unless data storage {ns}:temp _btn_data.equip_slot1_name run data modify storage {ns}:temp _btn_data.equip_slot1_name set value "?"',
    		f'execute unless data storage {ns}:temp _btn_data.equip_slot2_name run data modify storage {ns}:temp _btn_data.equip_slot2_name set value "?"',
    		f'execute unless data storage {ns}:temp _btn_data.main_gun_display run data modify storage {ns}:temp _btn_data.main_gun_display set from storage {ns}:temp _btn_data.main_gun',
    		f'execute unless data storage {ns}:temp _btn_data.secondary_gun_display run data modify storage {ns}:temp _btn_data.secondary_gun_display set value "None"',
    	])

    	# Helper to compute a trigger value and store it
    	def _compute_trig(field: str, base: int) -> str:
    		return (
    			f"execute store result score #trig {ns}.data run data get storage {ns}:temp _iter[0].id\n"
    			f"scoreboard players add #trig {ns}.data {base}\n"
    			f"execute store result storage {ns}:temp _btn_data.{field} int 1 run scoreboard players get #trig {ns}.data"
    		)

    	# Rich info component shared by the list-row tooltip and the manage-dialog body
    	def _ml_info(public_label: str) -> str:
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
    			'{"text":"' + _perk_concat + '","color":"light_purple"},'
    			'"\\n",'
    			'{"text":"\\u2665 $(likes) likes","color":"red"},'
    			'{"text":"  \\u2b50 $(favorites_count) favs","color":"yellow"},'
    			'"\\n",'
    			+ public_label
    			+ ']'
    		)

    	_ml_tooltip_pub = _ml_info('{"text":"Public","color":"green","italic":true},"\\n\\n",{"text":"\\u25b6 Click to manage","color":"dark_gray","italic":true}')
    	_ml_tooltip_priv = _ml_info('{"text":"Private","color":"red","italic":true},"\\n\\n",{"text":"\\u25b6 Click to manage","color":"dark_gray","italic":true}')

    	## my_loadouts/prep_btn - Each loadout becomes ONE list row that opens its manage submenu
    	self.func("multiplayer/my_loadouts/prep_btn", f"""
# Copy entry data for macro use
data modify storage {ns}:temp _btn_data set from storage {ns}:temp _iter[0]

# Compute the manage submenu trigger (TRIG_MANAGE_BASE + id)
{_compute_trig("manage_trig", TRIG_MANAGE_BASE)}

# Normalize and compute perk display
{_normalize_fields}

# Route to correct color variant based on public flag (green=public, red=private)
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 1 run function {ns}:v{version}/multiplayer/my_loadouts/add_btn_public with storage {ns}:temp _btn_data
execute if score #pub {ns}.data matches 0 run function {ns}:v{version}/multiplayer/my_loadouts/add_btn_private with storage {ns}:temp _btn_data
""")

    	## add_btn_public / add_btn_private - one row: name + ▶ arrow, opens the manage submenu
    	self.func("multiplayer/my_loadouts/add_btn_public", f"""$data modify storage {ns}:temp dialog.actions append value {{label:["",{{"text":"$(name)",color:"green"}},{{"text":"  \\u25b6","color":"dark_gray"}}],tooltip:{_ml_tooltip_pub},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(manage_trig)"}}}}
""")
    	self.func("multiplayer/my_loadouts/add_btn_private", f"""$data modify storage {ns}:temp dialog.actions append value {{label:["",{{"text":"$(name)",color:"red"}},{{"text":"  \\u25b6","color":"dark_gray"}}],tooltip:{_ml_tooltip_priv},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(manage_trig)"}}}}
""")

    	## ====================================================================
    	## MY LOADOUTS - per-loadout manage submenu (Use / Edit / Visibility / Default / Delete)
    	## ====================================================================
    	def _compute_trig_id(field: str, base: int) -> str:
    		"""Compute base + #loadout_id into _btn_data.<field> (manage submenu)."""
    		return (
    			f"scoreboard players operation #trig {ns}.data = #loadout_id {ns}.data\n"
    			f"scoreboard players add #trig {ns}.data {base}\n"
    			f"execute store result storage {ns}:temp _btn_data.{field} int 1 run scoreboard players get #trig {ns}.data"
    		)

    	## manage - Find the loadout by id, then build its management dialog
    	self.func("multiplayer/my_loadouts/manage", f"""
scoreboard players operation #loadout_id {ns}.data = @s {ns}.player.config
scoreboard players remove #loadout_id {ns}.data {TRIG_MANAGE_BASE}
data modify storage {ns}:temp _find_iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _find_iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/manage_find
""")

    	## manage_find - Recursive: locate loadout by id (and ownership), then prep its dialog
    	self.func("multiplayer/my_loadouts/manage_find", f"""
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _find_iter[0].id
execute store result score #entry_owner {ns}.data run data get storage {ns}:temp _find_iter[0].owner_pid
execute if score #entry_id {ns}.data = #loadout_id {ns}.data if score #entry_owner {ns}.data = @s {ns}.mp.pid run return run function {ns}:v{version}/multiplayer/my_loadouts/manage_prep
data remove storage {ns}:temp _find_iter[0]
execute if data storage {ns}:temp _find_iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/manage_find
""")

    	## manage_prep - Copy the found loadout, compute action triggers, normalize, build dialog
    	self.func("multiplayer/my_loadouts/manage_prep", f"""
data modify storage {ns}:temp _btn_data set from storage {ns}:temp _find_iter[0]
{_compute_trig_id("select_trig", TRIG_SELECT_BASE)}
{_compute_trig_id("edit_trig", TRIG_EDIT_BASE)}
{_compute_trig_id("vis_trig", TRIG_TOGGLE_VIS_BASE)}
{_compute_trig_id("delete_trig", TRIG_DELETE_BASE)}
{_compute_trig_id("default_trig", TRIG_SET_DEFAULT_BASE)}
{_normalize_fields}
execute store result score #pub {ns}.data run data get storage {ns}:temp _find_iter[0].public
execute if score #pub {ns}.data matches 1 run function {ns}:v{version}/multiplayer/my_loadouts/manage_build_public with storage {ns}:temp _btn_data
execute if score #pub {ns}.data matches 0 run function {ns}:v{version}/multiplayer/my_loadouts/manage_build_private with storage {ns}:temp _btn_data
""")

    	# Manage dialog body (rich info, no "click to manage" hint)
    	_manage_body_pub = _ml_info('{"text":"Public","color":"green","italic":true}')
    	_manage_body_priv = _ml_info('{"text":"Private","color":"red","italic":true}')

    	def _manage_dialog(vis_label: str, vis_tip: str, vis_color: str) -> str:
    		""" Shared manage dialog: Use / Edit / Toggle visibility / Set default / Delete + Back """
    		return (
    			'{type:"minecraft:multi_action",'
    			'title:{text:"$(name)",color:"gold",bold:true},'
    			'body:[{type:"minecraft:plain_message",contents:BODY}],'
    			'actions:['
    			f'{{label:{styled_text("▶ Use this loadout", color="green", bold="true")},tooltip:{{text:"Equip this loadout (applies on next spawn)"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(select_trig)"}}}},'
    			f'{{label:{styled_text("✏ Edit", color="gold")},tooltip:{{text:"Re-open the loadout editor pre-filled; saving overwrites this loadout",color:"yellow"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(edit_trig)"}}}},'
    			f'{{label:{{text:"{vis_label}",color:"{vis_color}"}},tooltip:{{text:"{vis_tip}"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(vis_trig)"}}}},'
    			f'{{label:{styled_text("⭐ Set as Default", color="yellow")},tooltip:{{text:"Auto-equip this loadout when a game starts"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(default_trig)"}}}},'
    			f'{{label:{styled_text("\U0001f5d1 Delete", color="red")},tooltip:{{text:"Permanently delete this loadout",color:"dark_red"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(delete_trig)"}}}}'
    			'],'
    			'columns:1,'
    			'after_action:"close",'
    			f'exit_action:{{label:"Back",action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MY_LOADOUTS}"}}}}'
    			'}'
    		)

    	self.func("multiplayer/my_loadouts/manage_build_public", f"""$data modify storage {ns}:temp dialog set value {_manage_dialog("Public -> Private", "Toggle this loadout to Private", "dark_aqua").replace("BODY", _manage_body_pub)}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")
    	self.func("multiplayer/my_loadouts/manage_build_private", f"""$data modify storage {ns}:temp dialog set value {_manage_dialog("Private -> Public", "Toggle this loadout to Public", "aqua").replace("BODY", _manage_body_priv)}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

    	## ====================================================================
    	## MARKETPLACE - Browse all public custom loadouts
    	## Organized as: [📋All] [⭐Favorites] [❤Best Liked] filter row,
    	##                then favorited public loadouts first, then the rest
    	## ====================================================================

    	def _marketplace_dialog_init() -> str:
    		return (
    			f'{{type:"minecraft:multi_action",'
    			f'title:{{text:"Marketplace",color:"light_purple",bold:true}},'
    			f'body:{{type:"minecraft:item",item:{{id:"minecraft:emerald"}},description:{{contents:{{text:"Browse public loadouts from all players",color:"gray"}}}},show_decoration:false,show_tooltip:true}},'
    			f'actions:[],'
    			f'columns:3,'
    			f'after_action:"close",'
    			f'exit_action:{{label:"Back",action:{{type:"run_command",command:"/trigger {ns}.player.config set 4"}}}}'
    			f'}}'
    		)

    	def _marketplace_filter_btns(active: str = "all") -> list[str]:
    		all_color = "aqua" if active == "all" else "white"
    		fav_color = "gold" if active == "fav" else "yellow"
    		likes_color = "red" if active == "likes" else "white"
    		return [
    			f'{{label:{styled_text("\U0001f4cb All", color=all_color, bold="true")},tooltip:{{text:"Show all public loadouts (your favorites first)"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MARKETPLACE_ALL}"}}}}',
    			f'{{label:{styled_text("\u2b50 Favorites", color=fav_color, bold="true")},tooltip:{{text:"Show only loadouts you favorited"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MARKETPLACE_FAV_ONLY}"}}}}',
    			f'{{label:{styled_text("\u2764 Best Liked", color=likes_color, bold="true")},tooltip:{{text:"Show all public loadouts sorted by most likes"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MARKETPLACE_LIKES}"}}}}',
    		]

    	## marketplace/browse - Default: favorites first, then the rest
    	self.func("multiplayer/marketplace/browse", f"""
# Initialize dialog
data modify storage {ns}:temp dialog set value {_marketplace_dialog_init()}

# Add filter/sort buttons (row 1: all / favorites / best liked)
data modify storage {ns}:temp dialog.actions append value {_marketplace_filter_btns("all")[0]}
data modify storage {ns}:temp dialog.actions append value {_marketplace_filter_btns("all")[1]}
data modify storage {ns}:temp dialog.actions append value {_marketplace_filter_btns("all")[2]}

# Load player favorites
function {ns}:v{version}/multiplayer/shared/load_player_favorites

# Pass 1: Public loadouts that are in player's favorites
data modify storage {ns}:temp _iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/build_list_favs

# Pass 2: Public loadouts NOT in player's favorites
data modify storage {ns}:temp _iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/build_list_rest

# Show dialog
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

    	## marketplace/browse_fav_only - Filter: only public + in player's favorites
    	self.func("multiplayer/marketplace/browse_fav_only", f"""
# Initialize dialog
data modify storage {ns}:temp dialog set value {_marketplace_dialog_init()}
data modify storage {ns}:temp dialog.title set value [{{text:"",color:"light_purple",bold:true}},{{text:"Marketplace"}}," \u2014 ",{{text:"Favorites"}}]

# Add filter/sort buttons (favorites tab active)
data modify storage {ns}:temp dialog.actions append value {_marketplace_filter_btns("fav")[0]}
data modify storage {ns}:temp dialog.actions append value {_marketplace_filter_btns("fav")[1]}
data modify storage {ns}:temp dialog.actions append value {_marketplace_filter_btns("fav")[2]}

# Load player favorites
function {ns}:v{version}/multiplayer/shared/load_player_favorites

# Only show public + in favorites
data modify storage {ns}:temp _iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/build_list_favs

# Show dialog
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

    	## marketplace/browse_likes - Sort by likes descending (find-max passes O(n^2), fine for small n)
    	self.func("multiplayer/marketplace/browse_likes", f"""
# Initialize dialog
data modify storage {ns}:temp dialog set value {_marketplace_dialog_init()}
data modify storage {ns}:temp dialog.title set value [{{text:"",color:"light_purple",bold:true}},{{text:"Marketplace"}}," \u2014 ",{{text:"Best Liked"}}]

# Add filter/sort buttons (likes tab active)
data modify storage {ns}:temp dialog.actions append value {_marketplace_filter_btns("likes")[0]}
data modify storage {ns}:temp dialog.actions append value {_marketplace_filter_btns("likes")[1]}
data modify storage {ns}:temp dialog.actions append value {_marketplace_filter_btns("likes")[2]}

# Load player favorites (used in prep_btn normalization)
function {ns}:v{version}/multiplayer/shared/load_player_favorites

# Collect all public loadouts into _sort_pool
data modify storage {ns}:temp _sort_pool set value []
data modify storage {ns}:temp _iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/sort_collect_pool

# Build buttons from highest to lowest likes
execute if data storage {ns}:temp _sort_pool[0] run function {ns}:v{version}/multiplayer/marketplace/sort_build_list

# Show dialog
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

    	## marketplace/build_list_favs - Pass 1: public + in favorites
    	self.func("multiplayer/marketplace/build_list_favs", f"""
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 1 run function {ns}:v{version}/multiplayer/shared/check_is_fav
execute if score #pub {ns}.data matches 1 if score #is_fav {ns}.data matches 1 run function {ns}:v{version}/multiplayer/marketplace/prep_btn

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/build_list_favs
""")

    	## marketplace/build_list_rest - Pass 2: public + NOT in favorites
    	self.func("multiplayer/marketplace/build_list_rest", f"""
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 1 run function {ns}:v{version}/multiplayer/shared/check_is_fav
execute if score #pub {ns}.data matches 1 if score #is_fav {ns}.data matches 0 run function {ns}:v{version}/multiplayer/marketplace/prep_btn

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/build_list_rest
""")

    	## marketplace/sort_collect_pool - Collect all public loadouts into _sort_pool for likes sort
    	self.func("multiplayer/marketplace/sort_collect_pool", f"""
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 1 run data modify storage {ns}:temp _sort_pool append from storage {ns}:temp _iter[0]

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/sort_collect_pool
""")

    	## marketplace/sort_build_list - Find max-likes entry, build its button, recurse
    	self.func("multiplayer/marketplace/sort_build_list", f"""
# Find max likes entry in _sort_pool
scoreboard players set #max_likes {ns}.data -1
data modify storage {ns}:temp _find_max_iter set from storage {ns}:temp _sort_pool
execute if data storage {ns}:temp _find_max_iter[0] run function {ns}:v{version}/multiplayer/marketplace/sort_find_max

# Temporarily set _iter[0] to the best entry so prep_btn can use it
data modify storage {ns}:temp _iter set value []
data modify storage {ns}:temp _iter append from storage {ns}:temp _sort_best
function {ns}:v{version}/multiplayer/marketplace/prep_btn

# Remove best entry from _sort_pool (match by id)
execute store result score #extract_id {ns}.data run data get storage {ns}:temp _sort_best.id
data modify storage {ns}:temp _pool_rebuild set from storage {ns}:temp _sort_pool
data modify storage {ns}:temp _sort_pool set value []
execute if data storage {ns}:temp _pool_rebuild[0] run function {ns}:v{version}/multiplayer/marketplace/sort_remove_best

# Recurse if pool still has entries
execute if data storage {ns}:temp _sort_pool[0] run function {ns}:v{version}/multiplayer/marketplace/sort_build_list
""")

    	## marketplace/sort_find_max - Recursive: scan _find_max_iter to find entry with most likes
    	self.func("multiplayer/marketplace/sort_find_max", f"""
execute unless data storage {ns}:temp _find_max_iter[0].likes run data modify storage {ns}:temp _find_max_iter[0].likes set value 0

execute store result score #this_likes {ns}.data run data get storage {ns}:temp _find_max_iter[0].likes
execute if score #this_likes {ns}.data > #max_likes {ns}.data run data modify storage {ns}:temp _sort_best set from storage {ns}:temp _find_max_iter[0]
execute if score #this_likes {ns}.data > #max_likes {ns}.data run scoreboard players operation #max_likes {ns}.data = #this_likes {ns}.data

data remove storage {ns}:temp _find_max_iter[0]
execute if data storage {ns}:temp _find_max_iter[0] run function {ns}:v{version}/multiplayer/marketplace/sort_find_max
""")

    	## marketplace/sort_remove_best - Rebuild _sort_pool excluding the entry with id = #extract_id
    	self.func("multiplayer/marketplace/sort_remove_best", f"""
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _pool_rebuild[0].id
execute unless score #entry_id {ns}.data = #extract_id {ns}.data run data modify storage {ns}:temp _sort_pool append from storage {ns}:temp _pool_rebuild[0]

data remove storage {ns}:temp _pool_rebuild[0]
execute if data storage {ns}:temp _pool_rebuild[0] run function {ns}:v{version}/multiplayer/marketplace/sort_remove_best
""")

    	## marketplace/prep_btn - Compute triggers, normalize fields, add buttons
    	self.func("multiplayer/marketplace/prep_btn", f"""
# Copy entry data for macro use
data modify storage {ns}:temp _btn_data set from storage {ns}:temp _iter[0]

# Compute triggers
{_compute_trig("select_trig", TRIG_SELECT_BASE)}
{_compute_trig("like_trig", TRIG_LIKE_BASE)}
{_compute_trig("fav_trig", TRIG_FAVORITE_BASE)}

# Normalize and compute perk display
{_normalize_fields}
execute unless data storage {ns}:temp _btn_data.owner_name run data modify storage {ns}:temp _btn_data.owner_name set value "?"

# Add buttons to dialog
function {ns}:v{version}/multiplayer/marketplace/add_btn with storage {ns}:temp _btn_data
""")

    	# Rich tooltip for MARKETPLACE buttons (includes owner name)
    	_mp_tooltip = (
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
    		'{"text":"' + _perk_concat + '","color":"light_purple"},'
    		'"\\n",'
    		'{"text":"\\u2665 $(likes) likes","color":"red"},'
    		'{"text":"  \\u2b50 $(favorites_count) favs","color":"yellow"},'
    		'"\\n",'
    		'{"text":"by $(owner_name)","color":"aqua","italic":true},'
    		'"\\n\\n",'
    		'{"text":"\\u25b6 Click to select","color":"dark_gray","italic":true}]'
    	)

    	## marketplace/add_btn - Macro: append 3 buttons (Select + Like + Favorite) with rich tooltip
    	self.func("multiplayer/marketplace/add_btn", f"""$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"$(name)",color:"green"}},tooltip:{_mp_tooltip},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(select_trig)"}}}}
$data modify storage {ns}:temp dialog.actions append value {{label:[{{text:"\u2b50 ",color:"gold"}},{{text:"Make Favorite",color:"yellow"}}],tooltip:{{text:"Add to favorites",color:"gold"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(fav_trig)"}}}}
$data modify storage {ns}:temp dialog.actions append value {{label:[{{text:"\u2665 ",color:"red"}},{{text:"Like the Loadout",color:"yellow"}}],tooltip:{{text:"Like this loadout",color:"yellow"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(like_trig)"}}}}
""")


def generate_browsing() -> None:
	""" Module-level entry (preserved signature); delegates to :class:`BrowsingGenerator`. """
	BrowsingGenerator()()


