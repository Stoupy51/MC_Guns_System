""" The operator dialog editing a mystery box pool: one weight per weapon, 0 to leave it out, for the global pool or the selected map. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.catalogs import PRIMARY_WEAPONS, SECONDARY_WEAPONS
from ....helpers import MGS_TAG

# Constants
MAX_WEIGHT: int = 20
""" Top of each weight slider. """


# Functions
def write_pool_menu() -> None:
	""" Write the two editors (global, selected map), their saves and the map override removal. """
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version
	base: str = f"{ns}:v{version}/zombies/mystery_box/pool"
	weapons: list[tuple[str, str]] = [(w.item_id, w.display_name) for w in (*PRIMARY_WEAPONS, *SECONDARY_WEAPONS)] + [("monkey_bomb", "Monkey Bomb")]

	inputs: str = "\n".join(
		f'data modify storage {ns}:temp dialog.inputs append value {{type:"minecraft:number_range",key:"{item_id}",label:"{name}",start:0,end:{MAX_WEIGHT},step:1,initial:0}}\n'
		f'data modify storage {ns}:temp dialog.inputs[-1].initial set from storage {ns}:temp _mb_cur[{{weapon_id:"{item_id}"}}].weight'
		for item_id, name in weapons
	)
	arguments: str = ",".join(f"{item_id}:$({item_id})" for item_id, _ in weapons)
	for target, title in (("global", "Mystery Box Pool"), ("map", "Mystery Box Pool of the Map")):
		write_versioned_function(f"zombies/mystery_box/pool/dialog_{target}", f"""
data modify storage {ns}:temp dialog set value {{type:"minecraft:multi_action",title:{{text:"{title}",color:"light_purple",bold:true}},body:[{{type:"minecraft:plain_message",contents:{{text:"Weight of each weapon in the box, 0 leaves it out","color":"gray"}}}}],inputs:[],actions:[{{label:{{text:"Save",color:"green"}},action:{{type:"minecraft:dynamic/run_command",template:"function {base}/save_{target} {{{arguments}}}"}}}}],columns:1,exit_action:{{label:{{translate:"gui.cancel"}}}}}}
{inputs}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	write_versioned_function("zombies/mystery_box/pool/edit_global", f"""
data modify storage {ns}:temp _mb_cur set from storage {ns}:config zombies.mystery_box_pool
function {base}/dialog_global
""")
	write_versioned_function("zombies/mystery_box/pool/edit_map", f"""
execute unless data storage {ns}:zombies game.map_id run return run tellraw @s [{MGS_TAG},{{"text":"Select a zombies map first.","color":"red"}}]
data modify storage {ns}:temp _mb_cur set from storage {ns}:config zombies.mystery_box_pool
function {base}/map_current with storage {ns}:zombies game
function {base}/dialog_map
""")
	write_versioned_function("zombies/mystery_box/pool/map_current", f'$data modify storage {ns}:temp _mb_cur set from storage {ns}:maps zombies[{{id:"$(map_id)"}}].mystery_box_pool')

	## A number_range value may arrive as a decimal, so each weight is stored back as an int.
	weights: str = "\n".join(
		f"$data modify storage {ns}:temp _mb_w set value $({item_id})\n"
		f'execute store result storage {ns}:temp _mb_pool[{{weapon_id:"{item_id}"}}].weight int 1 run data get storage {ns}:temp _mb_w'
		for item_id, _ in weapons
	)
	zeros: str = ",".join(f'{{weapon_id:"{item_id}",weight:0}}' for item_id, _ in weapons)
	write_versioned_function("zombies/mystery_box/pool/read_weights", f"""
data modify storage {ns}:temp _mb_pool set value [{zeros}]
{weights}
""")
	write_versioned_function("zombies/mystery_box/pool/save_global", f"""
$function {base}/read_weights {{{arguments}}}
data modify storage {ns}:config zombies.mystery_box_pool set from storage {ns}:temp _mb_pool
tellraw @s [{MGS_TAG},{{"text":"Global mystery box pool saved; it applies from the next game.","color":"green"}}]
""")
	write_versioned_function("zombies/mystery_box/pool/save_map", f"""
$function {base}/read_weights {{{arguments}}}
function {base}/store_map with storage {ns}:zombies game
""")
	write_versioned_function("zombies/mystery_box/pool/store_map", f"""
$data modify storage {ns}:maps zombies[{{id:"$(map_id)"}}].mystery_box_pool set from storage {ns}:temp _mb_pool
$tellraw @s [{MGS_TAG},{{"text":"Mystery box pool saved for $(map_id); it applies from the next game.","color":"green"}}]
""")
	write_versioned_function("zombies/mystery_box/pool/clear_map", f"""
execute unless data storage {ns}:zombies game.map_id run return run tellraw @s [{MGS_TAG},{{"text":"Select a zombies map first.","color":"red"}}]
function {base}/remove_map with storage {ns}:zombies game
""")
	write_versioned_function("zombies/mystery_box/pool/remove_map", f"""
$data remove storage {ns}:maps zombies[{{id:"$(map_id)"}}].mystery_box_pool
$tellraw @s [{MGS_TAG},{{"text":"$(map_id) uses the global mystery box pool again.","color":"green"}}]
""")

