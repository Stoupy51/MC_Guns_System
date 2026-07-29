""" The empty editor state, the editor's function path and the dialog skeleton filler. """
# Imports
from stewbeet import write_versioned_function


# Functions
# Empty editor state (display fields default to readable values so hub rows always render)
def empty_state() -> str:
	return (
		'{primary:"",primary_name:"None",primary_mag:"",primary_mag_count:1,'
		'primary_scope:"",primary_scope_name:"Iron Sights",primary_camo:"",primary_camo_name:"Default",primary_full:"",'
		'secondary:"",secondary_name:"None",secondary_mag:"",secondary_mag_count:0,'
		'secondary_scope:"",secondary_scope_name:"Iron Sights",secondary_camo:"",secondary_camo_name:"Default",secondary_full:"",'
		'equip_slot1:"",equip_slot1_name:"None",equip_slot1_camo:"",'
		'equip_slot2:"",equip_slot2_name:"None",equip_slot2_camo:"",'
		'knife_camo:"",knife_camo_name:"Default",'
		'perks:[]}'
	)

def editor_fn(ns: str, version: str) -> str:
	""" Return the versioned function path every editor cross-reference is written against.

	Args:
		ns (str):      The project namespace.
		version (str): The project version.
	Returns:
		str: The namespaced folder holding the editor's functions.

	Examples:
		>>> editor_fn("mgs", "1.0.0")
		'mgs:v1.0.0/multiplayer/editor'
	"""
	return f"{ns}:v{version}/multiplayer/editor"

def write_static_dialog(ns: str, version: str, name: str, title: str, hint: str, actions_snbt: str, columns: int = 2, guard: str = "") -> None:
	""" Write show_<name>: the shared skeleton filled in, then its own action list, then show. """
	fn: str = editor_fn(ns, version)
	write_versioned_function(f"multiplayer/editor/show_{name}", f"""
{guard}function {fn}/recompute_points
data modify storage {ns}:temp _dlg merge value {{title:'{{text:"Loadout - {title}",color:"gold",bold:true}}',hint:'{{text:"{hint}",color:"gray"}}',columns:{columns}}}
function {fn}/show_static_dialog with storage {ns}:temp _dlg
data modify storage {ns}:temp dialog.actions set value [{actions_snbt}]
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

