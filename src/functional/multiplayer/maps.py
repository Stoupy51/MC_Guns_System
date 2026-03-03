
# Imports
from stewbeet import Mem, write_versioned_function


def generate_maps() -> None:
	ns: str = Mem.ctx.project_id

	## ============================
	## Dynamic Map Registration
	## ============================
	write_versioned_function("multiplayer/register_map",
f"""
# Append map from mgs:input multiplayer.map to the maps list
# Expected format: {{name:"map_name", spawns:{{red:[x,y,z], blue:[x,y,z]}}, flags:{{red:[x,y,z], blue:[x,y,z]}}}}
data modify storage {ns}:multiplayer maps append from storage {ns}:input multiplayer.map
""")

