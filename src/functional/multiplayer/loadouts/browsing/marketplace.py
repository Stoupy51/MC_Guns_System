""" Browsing every public loadout, sorted by favourites or by likes. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.catalogs import (
	PICK10_TOTAL,
	TRIG_FAVORITE_BASE,
	TRIG_LIKE_BASE,
	TRIG_MARKETPLACE_ALL,
	TRIG_MARKETPLACE_FAV_ONLY,
	TRIG_MARKETPLACE_LIKES,
	TRIG_SELECT_BASE,
)
from ....helpers.text import Text
from .shared import PERK_CONCAT, compute_trig, normalize_btn_fields


# Functions
def write_marketplace() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Public custom loadouts: an All, Favorites and Best Liked filter row, then the player's favorites, then the rest.

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
			f'{{label:{Text.styled_text("\U0001f4cb All", color=all_color, bold="true")},tooltip:{{text:"Show all public loadouts (your favorites first)"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MARKETPLACE_ALL}"}}}}',
			f'{{label:{Text.styled_text("\u2b50 Favorites", color=fav_color, bold="true")},tooltip:{{text:"Show only loadouts you favorited"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MARKETPLACE_FAV_ONLY}"}}}}',
			f'{{label:{Text.styled_text("\u2764 Best Liked", color=likes_color, bold="true")},tooltip:{{text:"Show all public loadouts sorted by most likes"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_MARKETPLACE_LIKES}"}}}}',
		]

	## Favorites first, then the rest.
	write_versioned_function("multiplayer/marketplace/browse", f"""
data modify storage {ns}:temp dialog set value {marketplace_dialog_init()}

data modify storage {ns}:temp dialog.actions append value {marketplace_filter_btns("all")[0]}
data modify storage {ns}:temp dialog.actions append value {marketplace_filter_btns("all")[1]}
data modify storage {ns}:temp dialog.actions append value {marketplace_filter_btns("all")[2]}

function {ns}:v{version}/multiplayer/shared/load_player_favorites

data modify storage {ns}:temp _iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/build_list_favs

data modify storage {ns}:temp _iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/build_list_rest

function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## Only public loadouts the player favorited.
	write_versioned_function("multiplayer/marketplace/browse_fav_only", f"""
data modify storage {ns}:temp dialog set value {marketplace_dialog_init()}
data modify storage {ns}:temp dialog.title set value [{{text:"",color:"light_purple",bold:true}},{{text:"Marketplace"}}," \u2014 ",{{text:"Favorites"}}]

data modify storage {ns}:temp dialog.actions append value {marketplace_filter_btns("fav")[0]}
data modify storage {ns}:temp dialog.actions append value {marketplace_filter_btns("fav")[1]}
data modify storage {ns}:temp dialog.actions append value {marketplace_filter_btns("fav")[2]}

function {ns}:v{version}/multiplayer/shared/load_player_favorites

data modify storage {ns}:temp _iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/build_list_favs

function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## By likes, descending (repeated find-max, O(n^2), fine for small n).
	write_versioned_function("multiplayer/marketplace/browse_likes", f"""
data modify storage {ns}:temp dialog set value {marketplace_dialog_init()}
data modify storage {ns}:temp dialog.title set value [{{text:"",color:"light_purple",bold:true}},{{text:"Marketplace"}}," \u2014 ",{{text:"Best Liked"}}]

data modify storage {ns}:temp dialog.actions append value {marketplace_filter_btns("likes")[0]}
data modify storage {ns}:temp dialog.actions append value {marketplace_filter_btns("likes")[1]}
data modify storage {ns}:temp dialog.actions append value {marketplace_filter_btns("likes")[2]}

# prep_btn reads them.
function {ns}:v{version}/multiplayer/shared/load_player_favorites

data modify storage {ns}:temp _sort_pool set value []
data modify storage {ns}:temp _iter set from storage {ns}:multiplayer custom_loadouts
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/sort_collect_pool

execute if data storage {ns}:temp _sort_pool[0] run function {ns}:v{version}/multiplayer/marketplace/sort_build_list

function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	write_versioned_function("multiplayer/marketplace/build_list_favs", f"""
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 1 run function {ns}:v{version}/multiplayer/shared/check_is_fav
execute if score #pub {ns}.data matches 1 if score #is_fav {ns}.data matches 1 run function {ns}:v{version}/multiplayer/marketplace/prep_btn

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/build_list_favs
""")

	write_versioned_function("multiplayer/marketplace/build_list_rest", f"""
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 1 run function {ns}:v{version}/multiplayer/shared/check_is_fav
execute if score #pub {ns}.data matches 1 if score #is_fav {ns}.data matches 0 run function {ns}:v{version}/multiplayer/marketplace/prep_btn

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/build_list_rest
""")

	write_versioned_function("multiplayer/marketplace/sort_collect_pool", f"""
execute store result score #pub {ns}.data run data get storage {ns}:temp _iter[0].public
execute if score #pub {ns}.data matches 1 run data modify storage {ns}:temp _sort_pool append from storage {ns}:temp _iter[0]

data remove storage {ns}:temp _iter[0]
execute if data storage {ns}:temp _iter[0] run function {ns}:v{version}/multiplayer/marketplace/sort_collect_pool
""")

	## Find the most-liked entry, build its button, recurse.
	write_versioned_function("multiplayer/marketplace/sort_build_list", f"""
scoreboard players set #max_likes {ns}.data -1
data modify storage {ns}:temp _find_max_iter set from storage {ns}:temp _sort_pool
execute if data storage {ns}:temp _find_max_iter[0] run function {ns}:v{version}/multiplayer/marketplace/sort_find_max

# prep_btn reads _iter[0].
data modify storage {ns}:temp _iter set value []
data modify storage {ns}:temp _iter append from storage {ns}:temp _sort_best
function {ns}:v{version}/multiplayer/marketplace/prep_btn

# Matched by id.
execute store result score #extract_id {ns}.data run data get storage {ns}:temp _sort_best.id
data modify storage {ns}:temp _pool_rebuild set from storage {ns}:temp _sort_pool
data modify storage {ns}:temp _sort_pool set value []
execute if data storage {ns}:temp _pool_rebuild[0] run function {ns}:v{version}/multiplayer/marketplace/sort_remove_best

execute if data storage {ns}:temp _sort_pool[0] run function {ns}:v{version}/multiplayer/marketplace/sort_build_list
""")

	write_versioned_function("multiplayer/marketplace/sort_find_max", f"""
execute unless data storage {ns}:temp _find_max_iter[0].likes run data modify storage {ns}:temp _find_max_iter[0].likes set value 0

execute store result score #this_likes {ns}.data run data get storage {ns}:temp _find_max_iter[0].likes
execute if score #this_likes {ns}.data > #max_likes {ns}.data run data modify storage {ns}:temp _sort_best set from storage {ns}:temp _find_max_iter[0]
execute if score #this_likes {ns}.data > #max_likes {ns}.data run scoreboard players operation #max_likes {ns}.data = #this_likes {ns}.data

data remove storage {ns}:temp _find_max_iter[0]
execute if data storage {ns}:temp _find_max_iter[0] run function {ns}:v{version}/multiplayer/marketplace/sort_find_max
""")

	## Rebuild _sort_pool without the entry whose id is #extract_id.
	write_versioned_function("multiplayer/marketplace/sort_remove_best", f"""
execute store result score #entry_id {ns}.data run data get storage {ns}:temp _pool_rebuild[0].id
execute unless score #entry_id {ns}.data = #extract_id {ns}.data run data modify storage {ns}:temp _sort_pool append from storage {ns}:temp _pool_rebuild[0]

data remove storage {ns}:temp _pool_rebuild[0]
execute if data storage {ns}:temp _pool_rebuild[0] run function {ns}:v{version}/multiplayer/marketplace/sort_remove_best
""")

	write_versioned_function("multiplayer/marketplace/prep_btn", f"""
data modify storage {ns}:temp _btn_data set from storage {ns}:temp _iter[0]

{compute_trig(ns, "select_trig", TRIG_SELECT_BASE)}
{compute_trig(ns, "like_trig", TRIG_LIKE_BASE)}
{compute_trig(ns, "fav_trig", TRIG_FAVORITE_BASE)}

{normalize_btn_fields(ns)}
execute unless data storage {ns}:temp _btn_data.owner_name run data modify storage {ns}:temp _btn_data.owner_name set value "?"

function {ns}:v{version}/multiplayer/marketplace/add_btn with storage {ns}:temp _btn_data
""")

	# Marketplace tooltips also name the owner.
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

	## Select, Like and Favorite buttons, with the rich tooltip.
	write_versioned_function("multiplayer/marketplace/add_btn", f"""$data modify storage {ns}:temp dialog.actions append value {{label:{{text:"$(name)",color:"green"}},tooltip:{mp_tooltip},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(select_trig)"}}}}
$data modify storage {ns}:temp dialog.actions append value {{label:[{{text:"\u2b50 ",color:"gold"}},{{text:"Make Favorite",color:"yellow"}}],tooltip:{{text:"Add to favorites",color:"gold"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(fav_trig)"}}}}
$data modify storage {ns}:temp dialog.actions append value {{label:[{{text:"\u2665 ",color:"red"}},{{text:"Like the Loadout",color:"yellow"}}],tooltip:{{text:"Like this loadout",color:"yellow"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set $(like_trig)"}}}}
""")

