""" The bullet-icon font. """
# Imports
from stewbeet import Font, Mem, texture_mcmeta


# Functions
def write_assets() -> None:
	ns: str = Mem.ctx.project_id

	# Bullet font for the actionbar.
	textures_folder: str = Mem.ctx.meta.get("stewbeet", {}).get("textures_folder", "")
	font: Font = Mem.ctx.assets.fonts.setdefault(f"{ns}:icons", Font({"providers": []}))
	font.data["providers"].extend([
		{"type": "bitmap","file": f"{ns}:font/bullet_full.png","ascent": 7,"height": 9,"chars": ["A"]},
		{"type": "bitmap","file": f"{ns}:font/bullet_outline.png","ascent": 7,"height": 9,"chars": ["B"]},
	])
	for icon_name in ["bullet_outline", "bullet_full"]:
		Mem.ctx.assets[ns].textures[f"font/{icon_name}"] = texture_mcmeta(f"{textures_folder}/{icon_name}.png")

