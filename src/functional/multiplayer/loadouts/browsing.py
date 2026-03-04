
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from .catalogs import (
	PERKS,
	PICK10_TOTAL,
	TRIG_DELETE_BASE,
	TRIG_EDITOR_START,
	TRIG_FAVORITE_BASE,
	TRIG_LIKE_BASE,
	TRIG_MARKETPLACE_ALL,
	TRIG_MARKETPLACE_FAV_ONLY,
	TRIG_MARKETPLACE_LIKES,
	TRIG_MY_LOADOUTS,
	TRIG_MY_LOADOUTS_FAV_ONLY,
	TRIG_SELECT_BASE,
	TRIG_TOGGLE_VIS_BASE,
)


def generate_browsing() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## ====================================================================
	## SHARED HELPERS - player favorites loading & is-fav check
	## ====================================================================

	## shared/load_player_favorites - Copy current player's favorites list into _cur_favorites
	write_versioned_function("multiplayer/shared/load_player_favorites",
f"""
# Default to empty favorites
data modify storage {ns}:temp _cur_favorites set value []
# Scan player_data for our PID entry and copy its favorites list
data modify storage {ns}:temp _pd_iter set from storage {ns}:multiplayer player_data
execute if data storage {ns}:temp _pd_iter[0] run function {ns}:v{version}/multiplayer/shared/load_fav_iter
""")

	## shared/load_fav_iter - Recursive: find our entry by PID and copy favorites
	write_versioned_function("multiplayer/shared/load_fav_iter",
f"""
execute store result score #pd_pid {ns}.data run data get storage {ns}:temp _pd_iter[0].pid
execute if score #pd_pid {ns}.data = @s {ns}.mp.pid run data modify storage {ns}:temp _cur_favorites set from storage {ns}:temp _pd_iter[0].favorites
data remove storage {ns}:temp _pd_iter[0]
# Stop early once our entry is found
execute unless score #pd_pid {ns}.data = @s {ns}.mp.pid if data storage {ns}:temp _pd_iter[0] run function {ns}:v{version}/multiplayer/shared/load_fav_iter
""")

	## shared/check_is_fav - Sets #is_fav = 1 if _iter[0].id is in _cur_favorites, else 0
	write_versioned_function("multiplayer/shared/check_is_fav",
f"""
execute store result score #check_id {ns}.data run data get storage {ns}:temp _iter[0].id
data modify storage {ns}:temp _fav_check set from storage {ns}:temp _cur_favorites
scoreboard players set #is_fav {ns}.data 0
execute if data storage {ns}:temp _fav_check[0] run function {ns}:v{version}/multiplayer/shared/check_fav_iter
""")

	## shared/check_fav_iter - Recursive: compare each _fav_check entry against #check_id
	write_versioned_function("multiplayer/shared/check_fav_iter",
f"""
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
			f'body:{{type:"minecraft:item",item:{{id:"minecraft:written_book"}},description:{{contents:{{text:"Manage your custom loadouts.",color:"gray"}}}},show_decoration:false,show_tooltip:true}},'
			f'actions:[],'
			f'columns:3,'
			f'after_action:"close",'
			f'exit_action:{{label:"Back",action:{{type:"run_command",command:"/trigger {ns}.player.config set 4"}}}}'
			f'}}'
		)

	def _my_loadouts_filter_btns(active: str = "all") -> list[str]:
		"""Return the 3 filter button SNBT entries for My Loadouts."""
		fav_color = "gold" if active == "fav" else "yellow"
		all_color = "aqua" if active == "all" else "white"
		return [
			f'{{label:{{text:"\u2b50 Favorites",color:"{fav_color}",bold:true}},tooltip:{{text:"Show only your favorited loadouts"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MY_LOADOUTS_FAV_ONLY}"}}}}',
			f'{{label:{{text:"\U0001f4cb All",color:"{all_color}",bold:true}},tooltip:{{text:"Show all your loadouts (favorites first, then private, then public)"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MY_LOADOUTS}"}}}}',
			f'{{label:{{text:"\u271a Create",color:"green",bold:true}},tooltip:{{text:"Build a new custom loadout from scratch"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_EDITOR_START}"}}}}',
		]

	## my_loadouts/browse - Default: 3-pass build (favorites → privates → publics) + filter row
	write_versioned_function("multiplayer/my_loadouts/browse",
f"""
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
	write_versioned_function("multiplayer/my_loadouts/browse_fav_only",
f"""
# Initialize dialog
data modify storage {ns}:temp dialog set value {_my_loadouts_dialog_init()}
data modify storage {ns}:temp dialog.title set value {{text:"My Loadouts \u2014 Favorites",color:"gold",bold:true}}

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
	write_versioned_function("multiplayer/my_loadouts/build_list_favs",
f"""
execute store result score #entry_owner {ns}.data run data get storage {ns}:temp _iter[0].owner_pid
execute if score #entry_owner {ns}.data = @s {ns}.mp.pid run function {ns}:v{version}/multiplayer/shared/check_is_fav
execute if score #entry_owner {ns}.data = @s {ns}.mp.pid if score #is_fav {ns}.data matches 1 run function {ns}:v{version}/multiplayer/my_loadouts/prep_btn

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/build_list_favs
""")

	## my_loadouts/build_list_privates - Pass 2: own private loadouts NOT in favorites
	write_versioned_function("multiplayer/my_loadouts/build_list_privates",
f"""
execute store result score #entry_owner {ns}.data run data get storage {ns}:temp _iter[0].owner_pid
execute if score #entry_owner {ns}.data = @s {ns}.mp.pid run function {ns}:v{version}/multiplayer/my_loadouts/check_private_not_fav

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/build_list_privates
""")

	## check_private_not_fav - For own entries: only add if private AND not in favorites
	write_versioned_function("multiplayer/my_loadouts/check_private_not_fav",
f"""
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 0 run function {ns}:v{version}/multiplayer/shared/check_is_fav
execute if score #pub {ns}.data matches 0 if score #is_fav {ns}.data matches 0 run function {ns}:v{version}/multiplayer/my_loadouts/prep_btn
""")

	## my_loadouts/build_list_publics - Pass 3: own public loadouts NOT in favorites
	write_versioned_function("multiplayer/my_loadouts/build_list_publics",
f"""
execute store result score #entry_owner {ns}.data run data get storage {ns}:temp _iter[0].owner_pid
execute if score #entry_owner {ns}.data = @s {ns}.mp.pid run function {ns}:v{version}/multiplayer/my_loadouts/check_public_not_fav

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/my_loadouts/build_list_publics
""")

	## check_public_not_fav - For own entries: only add if public AND not in favorites
	write_versioned_function("multiplayer/my_loadouts/check_public_not_fav",
f"""
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

	## my_loadouts/prep_btn - Normalize fields, compute triggers, route to correct btn macro
	write_versioned_function("multiplayer/my_loadouts/prep_btn",
f"""
# Copy entry data for macro use (all stored fields come along)
data modify storage {ns}:temp _btn_data set from storage {ns}:temp _iter[0]

# Compute select trigger: {TRIG_SELECT_BASE} + id
execute store result score #trig {ns}.data run data get storage {ns}:temp _iter[0].id
scoreboard players add #trig {ns}.data {TRIG_SELECT_BASE}
execute store result storage {ns}:temp _btn_data.select_trig int 1 run scoreboard players get #trig {ns}.data

# Compute toggle visibility trigger: {TRIG_TOGGLE_VIS_BASE} + id
execute store result score #trig {ns}.data run data get storage {ns}:temp _iter[0].id
scoreboard players add #trig {ns}.data {TRIG_TOGGLE_VIS_BASE}
execute store result storage {ns}:temp _btn_data.vis_trig int 1 run scoreboard players get #trig {ns}.data

# Compute delete trigger: {TRIG_DELETE_BASE} + id
execute store result score #trig {ns}.data run data get storage {ns}:temp _iter[0].id
scoreboard players add #trig {ns}.data {TRIG_DELETE_BASE}
execute store result storage {ns}:temp _btn_data.delete_trig int 1 run scoreboard players get #trig {ns}.data

# Compute perks_count from perks list size
execute unless data storage {ns}:temp _btn_data.perks run data modify storage {ns}:temp _btn_data.perks set value []
execute store result storage {ns}:temp _btn_data.perks_count int 1 run data get storage {ns}:temp _btn_data.perks

# Build per-perk display names for tooltip
{_perk_disp}

# Normalize optional fields (backwards compat for pre-update loadouts)
execute unless data storage {ns}:temp _btn_data.points_used run data modify storage {ns}:temp _btn_data.points_used set value 0
execute unless data storage {ns}:temp _btn_data.favorites_count run data modify storage {ns}:temp _btn_data.favorites_count set value 0
execute unless data storage {ns}:temp _btn_data.likes run data modify storage {ns}:temp _btn_data.likes set value 0
execute unless data storage {ns}:temp _btn_data.equip_slot1_name run data modify storage {ns}:temp _btn_data.equip_slot1_name set value "?"
execute unless data storage {ns}:temp _btn_data.equip_slot2_name run data modify storage {ns}:temp _btn_data.equip_slot2_name set value "?"
execute unless data storage {ns}:temp _btn_data.main_gun_display run data modify storage {ns}:temp _btn_data.main_gun_display set from storage {ns}:temp _btn_data.main_gun
execute unless data storage {ns}:temp _btn_data.secondary_gun_display run data modify storage {ns}:temp _btn_data.secondary_gun_display set value "None"

# Route to correct color variant based on public flag (green=public, red=private)
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 1 run function {ns}:v{version}/multiplayer/my_loadouts/add_btn_public with storage {ns}:temp _btn_data
execute if score #pub {ns}.data matches 0 run function {ns}:v{version}/multiplayer/my_loadouts/add_btn_private with storage {ns}:temp _btn_data
""")

	# Rich tooltip for MY_LOADOUTS buttons
	_ml_tooltip_pub = (
		'["",{"text":"$(main_gun_display)","color":"green"},'
		'{"text":" x$(primary_mag_count) mags","color":"dark_green"},'
		'"\\n",'
		'{"text":"$(secondary_gun_display)","color":"yellow"},'
		'{"text":" x$(secondary_mag_count) mags","color":"gold"},'
		'"\\n",'
		'{"text":"Grenades: ","color":"gray"},'
		'{"text":"$(equip_slot1_name)","color":"aqua"},'
		'{"text":" + $(equip_slot2_name)","color":"aqua"},'
		'"\\n",'
		'{"text":"Points: ","color":"white"},'
		f'{{"text":"$(points_used)/{PICK10_TOTAL}pts","color":"gold"}},'
		'{"text":"  Perks: ","color":"white"},'
		'{"text":"$(perks_count)","color":"light_purple"},'
		'{"text":"$(perk0)$(perk1)$(perk2)","color":"light_purple"},'
		'"\\n",'
		'{"text":"\\u2665 $(likes) likes","color":"red"},'
		'{"text":"  \\u2b50 $(favorites_count) favs","color":"yellow"},'
		'"\\n",'
		'{"text":"Public","color":"green","italic":true},'
		'"\\n\\n",'
		'{"text":"\\u25b6 Click to select","color":"dark_gray","italic":true}]'
	)
	_ml_tooltip_priv = _ml_tooltip_pub.replace(
		'{"text":"Public","color":"green","italic":true}',
		'{"text":"Private","color":"red","italic":true}',
	)

	## my_loadouts/add_btn_public - Macro: green name (public loadout), rich tooltip
	write_versioned_function("multiplayer/my_loadouts/add_btn_public",
f"""$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"$(name)",color:"green"}},tooltip:{_ml_tooltip_pub},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(select_trig)"}}}}
$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"Public -> Private",color:"dark_aqua"}},tooltip:{{text:"Toggle this loadout to Private",color:"red"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(vis_trig)"}}}}
$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"\U0001f5d1 Delete",color:"red"}},tooltip:{{text:"Permanently delete this loadout",color:"dark_red"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(delete_trig)"}}}}
""")

	## my_loadouts/add_btn_private - Macro: red name (private loadout), rich tooltip
	write_versioned_function("multiplayer/my_loadouts/add_btn_private",
f"""$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"$(name)",color:"red"}},tooltip:{_ml_tooltip_priv},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(select_trig)"}}}}
$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"Private -> Public",color:"aqua"}},tooltip:{{text:"Toggle this loadout to Public",color:"green"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(vis_trig)"}}}}
$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"\U0001f5d1 Delete",color:"red"}},tooltip:{{text:"Permanently delete this loadout",color:"dark_red"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(delete_trig)"}}}}
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
			f'body:{{type:"minecraft:item",item:{{id:"minecraft:emerald"}},description:{{contents:{{text:"Browse public loadouts from all players.",color:"gray"}}}},show_decoration:false,show_tooltip:true}},'
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
			f'{{label:{{text:"\U0001f4cb All",color:"{all_color}",bold:true}},tooltip:{{text:"Show all public loadouts (your favorites first)"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MARKETPLACE_ALL}"}}}}',
			f'{{label:{{text:"\u2b50 Favorites",color:"{fav_color}",bold:true}},tooltip:{{text:"Show only loadouts you favorited"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MARKETPLACE_FAV_ONLY}"}}}}',
			f'{{label:{{text:"\u2764 Best Liked",color:"{likes_color}",bold:true}},tooltip:{{text:"Show all public loadouts sorted by most likes"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MARKETPLACE_LIKES}"}}}}',
		]

	## marketplace/browse - Default: favorites first, then the rest
	write_versioned_function("multiplayer/marketplace/browse",
f"""
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
	write_versioned_function("multiplayer/marketplace/browse_fav_only",
f"""
# Initialize dialog
data modify storage {ns}:temp dialog set value {_marketplace_dialog_init()}
data modify storage {ns}:temp dialog.title set value {{text:"Marketplace \u2014 Favorites",color:"light_purple",bold:true}}

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
	write_versioned_function("multiplayer/marketplace/browse_likes",
f"""
# Initialize dialog
data modify storage {ns}:temp dialog set value {_marketplace_dialog_init()}
data modify storage {ns}:temp dialog.title set value {{text:"Marketplace \u2014 Best Liked",color:"light_purple",bold:true}}

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
	write_versioned_function("multiplayer/marketplace/build_list_favs",
f"""
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 1 run function {ns}:v{version}/multiplayer/shared/check_is_fav
execute if score #pub {ns}.data matches 1 if score #is_fav {ns}.data matches 1 run function {ns}:v{version}/multiplayer/marketplace/prep_btn

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/build_list_favs
""")

	## marketplace/build_list_rest - Pass 2: public + NOT in favorites
	write_versioned_function("multiplayer/marketplace/build_list_rest",
f"""
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 1 run function {ns}:v{version}/multiplayer/shared/check_is_fav
execute if score #pub {ns}.data matches 1 if score #is_fav {ns}.data matches 0 run function {ns}:v{version}/multiplayer/marketplace/prep_btn

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/build_list_rest
""")

	## marketplace/sort_collect_pool - Collect all public loadouts into _sort_pool for likes sort
	write_versioned_function("multiplayer/marketplace/sort_collect_pool",
f"""
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 1 run data modify storage {ns}:temp _sort_pool append from storage {ns}:temp _iter[0]

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/sort_collect_pool
""")

	## marketplace/sort_build_list - Find max-likes entry, build its button, recurse
	write_versioned_function("multiplayer/marketplace/sort_build_list",
f"""
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
	write_versioned_function("multiplayer/marketplace/sort_find_max",
f"""
execute unless data storage {ns}:temp _find_max_iter[0].likes run data modify storage {ns}:temp _find_max_iter[0].likes set value 0

execute store result score #this_likes {ns}.data run data get storage {ns}:temp _find_max_iter[0].likes
execute if score #this_likes {ns}.data > #max_likes {ns}.data run data modify storage {ns}:temp _sort_best set from storage {ns}:temp _find_max_iter[0]
execute if score #this_likes {ns}.data > #max_likes {ns}.data run scoreboard players operation #max_likes {ns}.data = #this_likes {ns}.data

data remove storage {ns}:temp _find_max_iter[0]
execute if data storage {ns}:temp _find_max_iter[0] run function {ns}:v{version}/multiplayer/marketplace/sort_find_max
""")

	## marketplace/sort_remove_best - Rebuild _sort_pool excluding the entry with id = #extract_id
	write_versioned_function("multiplayer/marketplace/sort_remove_best",
f"""
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _pool_rebuild[0].id
execute unless score #entry_id {ns}.data = #extract_id {ns}.data run data modify storage {ns}:temp _sort_pool append from storage {ns}:temp _pool_rebuild[0]

data remove storage {ns}:temp _pool_rebuild[0]
execute if data storage {ns}:temp _pool_rebuild[0] run function {ns}:v{version}/multiplayer/marketplace/sort_remove_best
""")

	## marketplace/prep_btn - Compute triggers, normalize fields, add buttons
	write_versioned_function("multiplayer/marketplace/prep_btn",
f"""
# Copy entry data for macro use
data modify storage {ns}:temp _btn_data set from storage {ns}:temp _iter[0]

# Compute select trigger: {TRIG_SELECT_BASE} + id
execute store result score #trig {ns}.data run data get storage {ns}:temp _iter[0].id
scoreboard players add #trig {ns}.data {TRIG_SELECT_BASE}
execute store result storage {ns}:temp _btn_data.select_trig int 1 run scoreboard players get #trig {ns}.data

# Compute like trigger: {TRIG_LIKE_BASE} + id
execute store result score #trig {ns}.data run data get storage {ns}:temp _iter[0].id
scoreboard players add #trig {ns}.data {TRIG_LIKE_BASE}
execute store result storage {ns}:temp _btn_data.like_trig int 1 run scoreboard players get #trig {ns}.data

# Compute favorite trigger: {TRIG_FAVORITE_BASE} + id
execute store result score #trig {ns}.data run data get storage {ns}:temp _iter[0].id
scoreboard players add #trig {ns}.data {TRIG_FAVORITE_BASE}
execute store result storage {ns}:temp _btn_data.fav_trig int 1 run scoreboard players get #trig {ns}.data

# Compute perks_count from perks list size
execute unless data storage {ns}:temp _btn_data.perks run data modify storage {ns}:temp _btn_data.perks set value []
execute store result storage {ns}:temp _btn_data.perks_count int 1 run data get storage {ns}:temp _btn_data.perks

# Build per-perk display names for tooltip
{_perk_disp}

# Normalize optional fields (backwards compat for pre-update loadouts)
execute unless data storage {ns}:temp _btn_data.points_used run data modify storage {ns}:temp _btn_data.points_used set value 0
execute unless data storage {ns}:temp _btn_data.favorites_count run data modify storage {ns}:temp _btn_data.favorites_count set value 0
execute unless data storage {ns}:temp _btn_data.likes run data modify storage {ns}:temp _btn_data.likes set value 0
execute unless data storage {ns}:temp _btn_data.equip_slot1_name run data modify storage {ns}:temp _btn_data.equip_slot1_name set value "?"
execute unless data storage {ns}:temp _btn_data.equip_slot2_name run data modify storage {ns}:temp _btn_data.equip_slot2_name set value "?"
execute unless data storage {ns}:temp _btn_data.main_gun_display run data modify storage {ns}:temp _btn_data.main_gun_display set from storage {ns}:temp _btn_data.main_gun
execute unless data storage {ns}:temp _btn_data.secondary_gun_display run data modify storage {ns}:temp _btn_data.secondary_gun_display set value "None"
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
		'{"text":"Grenades: ","color":"gray"},'
		'{"text":"$(equip_slot1_name)","color":"aqua"},'
		'{"text":" + $(equip_slot2_name)","color":"aqua"},'
		'"\\n",'
		'{"text":"Points: ","color":"white"},'
		f'{{"text":"$(points_used)/{PICK10_TOTAL}pts","color":"gold"}},'
		'{"text":"  Perks: ","color":"white"},'
		'{"text":"$(perks_count)","color":"light_purple"},'
		'{"text":"$(perk0)$(perk1)$(perk2)","color":"light_purple"},'
		'"\\n",'
		'{"text":"\\u2665 $(likes) likes","color":"red"},'
		'{"text":"  \\u2b50 $(favorites_count) favs","color":"yellow"},'
		'"\\n",'
		'{"text":"by $(owner_name)","color":"aqua","italic":true},'
		'"\\n\\n",'
		'{"text":"\\u25b6 Click to select","color":"dark_gray","italic":true}]'
	)

	## marketplace/add_btn - Macro: append 3 buttons (Select + Like + Favorite) with rich tooltip
	write_versioned_function("multiplayer/marketplace/add_btn",
f"""$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"$(name)",color:"green"}},tooltip:{_mp_tooltip},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(select_trig)"}}}}
$data modify storage {ns}:temp dialog.actions append value {{label:[{{text:"\u2b50 ",color:"gold"}},{{text:"Make Favorite",color:"yellow"}}],tooltip:{{text:"Add to favorites",color:"gold"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(fav_trig)"}}}}
$data modify storage {ns}:temp dialog.actions append value {{label:[{{text:"\u2665 ",color:"red"}},{{text:"Like the Loadout",color:"yellow"}}],tooltip:{{text:"Like this loadout",color:"yellow"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(like_trig)"}}}}
""")

