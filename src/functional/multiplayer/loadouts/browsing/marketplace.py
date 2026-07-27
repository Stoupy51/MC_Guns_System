""" Browsing every public loadout, sorted by favourites or by likes. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import FunctionalHelpers
from ..catalogs import PICK10_TOTAL, TRIG_FAVORITE_BASE, TRIG_LIKE_BASE, TRIG_MARKETPLACE_ALL, TRIG_MARKETPLACE_FAV_ONLY, TRIG_MARKETPLACE_LIKES, TRIG_SELECT_BASE
from .shared import PERK_CONCAT, compute_trig, normalize_btn_fields


# Functions
def write_marketplace() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## MARKETPLACE - Browse all public custom loadouts Organized as: [📋All] [⭐Favorites] [❤Best Liked] filter row, then favorited public loadouts first, then the rest

	def marketplace_dialog_init() -> str:
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

	def marketplace_filter_btns(active: str = "all") -> list[str]:
		all_color = "aqua" if active == "all" else "white"
		fav_color = "gold" if active == "fav" else "yellow"
		likes_color = "red" if active == "likes" else "white"
		return [
			f'{{label:{FunctionalHelpers.styled_text("\U0001f4cb All", color=all_color, bold="true")},tooltip:{{text:"Show all public loadouts (your favorites first)"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MARKETPLACE_ALL}"}}}}',
			f'{{label:{FunctionalHelpers.styled_text("\u2b50 Favorites", color=fav_color, bold="true")},tooltip:{{text:"Show only loadouts you favorited"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MARKETPLACE_FAV_ONLY}"}}}}',
			f'{{label:{FunctionalHelpers.styled_text("\u2764 Best Liked", color=likes_color, bold="true")},tooltip:{{text:"Show all public loadouts sorted by most likes"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MARKETPLACE_LIKES}"}}}}',
		]

	## marketplace/browse - Default: favorites first, then the rest
	write_versioned_function("multiplayer/marketplace/browse", f"""
# Initialize dialog
data modify storage {ns}:temp dialog set value {marketplace_dialog_init()}

# Add filter/sort buttons (row 1: all / favorites / best liked)
data modify storage {ns}:temp dialog.actions append value {marketplace_filter_btns("all")[0]}
data modify storage {ns}:temp dialog.actions append value {marketplace_filter_btns("all")[1]}
data modify storage {ns}:temp dialog.actions append value {marketplace_filter_btns("all")[2]}

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
	write_versioned_function("multiplayer/marketplace/browse_fav_only", f"""
# Initialize dialog
data modify storage {ns}:temp dialog set value {marketplace_dialog_init()}
data modify storage {ns}:temp dialog.title set value [{{text:"",color:"light_purple",bold:true}},{{text:"Marketplace"}}," \u2014 ",{{text:"Favorites"}}]

# Add filter/sort buttons (favorites tab active)
data modify storage {ns}:temp dialog.actions append value {marketplace_filter_btns("fav")[0]}
data modify storage {ns}:temp dialog.actions append value {marketplace_filter_btns("fav")[1]}
data modify storage {ns}:temp dialog.actions append value {marketplace_filter_btns("fav")[2]}

# Load player favorites
function {ns}:v{version}/multiplayer/shared/load_player_favorites

# Only show public + in favorites
data modify storage {ns}:temp _iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/build_list_favs

# Show dialog
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## marketplace/browse_likes - Sort by likes descending (find-max passes O(n^2), fine for small n)
	write_versioned_function("multiplayer/marketplace/browse_likes", f"""
# Initialize dialog
data modify storage {ns}:temp dialog set value {marketplace_dialog_init()}
data modify storage {ns}:temp dialog.title set value [{{text:"",color:"light_purple",bold:true}},{{text:"Marketplace"}}," \u2014 ",{{text:"Best Liked"}}]

# Add filter/sort buttons (likes tab active)
data modify storage {ns}:temp dialog.actions append value {marketplace_filter_btns("likes")[0]}
data modify storage {ns}:temp dialog.actions append value {marketplace_filter_btns("likes")[1]}
data modify storage {ns}:temp dialog.actions append value {marketplace_filter_btns("likes")[2]}

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
	write_versioned_function("multiplayer/marketplace/build_list_favs", f"""
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 1 run function {ns}:v{version}/multiplayer/shared/check_is_fav
execute if score #pub {ns}.data matches 1 if score #is_fav {ns}.data matches 1 run function {ns}:v{version}/multiplayer/marketplace/prep_btn

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/build_list_favs
""")

	## marketplace/build_list_rest - Pass 2: public + NOT in favorites
	write_versioned_function("multiplayer/marketplace/build_list_rest", f"""
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 1 run function {ns}:v{version}/multiplayer/shared/check_is_fav
execute if score #pub {ns}.data matches 1 if score #is_fav {ns}.data matches 0 run function {ns}:v{version}/multiplayer/marketplace/prep_btn

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/build_list_rest
""")

	## marketplace/sort_collect_pool - Collect all public loadouts into _sort_pool for likes sort
	write_versioned_function("multiplayer/marketplace/sort_collect_pool", f"""
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 1 run data modify storage {ns}:temp _sort_pool append from storage {ns}:temp _iter[0]

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/sort_collect_pool
""")

	## marketplace/sort_build_list - Find max-likes entry, build its button, recurse
	write_versioned_function("multiplayer/marketplace/sort_build_list", f"""
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
	write_versioned_function("multiplayer/marketplace/sort_find_max", f"""
execute unless data storage {ns}:temp _find_max_iter[0].likes run data modify storage {ns}:temp _find_max_iter[0].likes set value 0

execute store result score #this_likes {ns}.data run data get storage {ns}:temp _find_max_iter[0].likes
execute if score #this_likes {ns}.data > #max_likes {ns}.data run data modify storage {ns}:temp _sort_best set from storage {ns}:temp _find_max_iter[0]
execute if score #this_likes {ns}.data > #max_likes {ns}.data run scoreboard players operation #max_likes {ns}.data = #this_likes {ns}.data

data remove storage {ns}:temp _find_max_iter[0]
execute if data storage {ns}:temp _find_max_iter[0] run function {ns}:v{version}/multiplayer/marketplace/sort_find_max
""")

	## marketplace/sort_remove_best - Rebuild _sort_pool excluding the entry with id = #extract_id
	write_versioned_function("multiplayer/marketplace/sort_remove_best", f"""
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _pool_rebuild[0].id
execute unless score #entry_id {ns}.data = #extract_id {ns}.data run data modify storage {ns}:temp _sort_pool append from storage {ns}:temp _pool_rebuild[0]

data remove storage {ns}:temp _pool_rebuild[0]
execute if data storage {ns}:temp _pool_rebuild[0] run function {ns}:v{version}/multiplayer/marketplace/sort_remove_best
""")

	## marketplace/prep_btn - Compute triggers, normalize fields, add buttons
	write_versioned_function("multiplayer/marketplace/prep_btn", f"""
# Copy entry data for macro use
data modify storage {ns}:temp _btn_data set from storage {ns}:temp _iter[0]

# Compute triggers
{compute_trig(ns, "select_trig", TRIG_SELECT_BASE)}
{compute_trig(ns, "like_trig", TRIG_LIKE_BASE)}
{compute_trig(ns, "fav_trig", TRIG_FAVORITE_BASE)}

# Normalize and compute perk display
{normalize_btn_fields(ns)}
execute unless data storage {ns}:temp _btn_data.owner_name run data modify storage {ns}:temp _btn_data.owner_name set value "?"

# Add buttons to dialog
function {ns}:v{version}/multiplayer/marketplace/add_btn with storage {ns}:temp _btn_data
""")

	# Rich tooltip for MARKETPLACE buttons (includes owner name)
	mp_tooltip = (
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
		'{"text":"by $(owner_name)","color":"aqua","italic":true},'
		'"\\n\\n",'
		'{"text":"\\u25b6 Click to select","color":"dark_gray","italic":true}]'
	)

	## marketplace/add_btn - Macro: append 3 buttons (Select + Like + Favorite) with rich tooltip
	write_versioned_function("multiplayer/marketplace/add_btn", f"""$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"$(name)",color:"green"}},tooltip:{mp_tooltip},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(select_trig)"}}}}
$data modify storage {ns}:temp dialog.actions append value {{label:[{{text:"\u2b50 ",color:"gold"}},{{text:"Make Favorite",color:"yellow"}}],tooltip:{{text:"Add to favorites",color:"gold"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(fav_trig)"}}}}
$data modify storage {ns}:temp dialog.actions append value {{label:[{{text:"\u2665 ",color:"red"}},{{text:"Like the Loadout",color:"yellow"}}],tooltip:{{text:"Like this loadout",color:"yellow"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(like_trig)"}}}}
""")

