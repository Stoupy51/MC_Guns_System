""" The bullet-icon font and the random-weapon utility. """
# Imports
from stewbeet import Font, Mem, texture_mcmeta, write_versioned_function


# Functions
def write_assets() -> None:
	ns: str = Mem.ctx.project_id

	# Add bullet font (for actionbar)
	textures_folder: str = Mem.ctx.meta.get("stewbeet", {}).get("textures_folder", "")
	font: Font = Mem.ctx.assets.fonts.setdefault(f"{ns}:icons", Font({"providers": []}))
	font.data["providers"].extend([
		{"type": "bitmap","file": f"{ns}:font/bullet_full.png","ascent": 7,"height": 9,"chars": ["A"]},
		{"type": "bitmap","file": f"{ns}:font/bullet_outline.png","ascent": 7,"height": 9,"chars": ["B"]},
	])
	for icon_name in ["bullet_outline", "bullet_full"]:
		Mem.ctx.assets[ns].textures[f"font/{icon_name}"] = texture_mcmeta(f"{textures_folder}/{icon_name}.png")

	# Random weapon function
	write_versioned_function("utils/random_weapon", f"""
execute store result score #random {ns}.data run random value 1..31
$execute if score #random {ns}.data matches 1 run loot replace entity @s $(slot) loot {ns}:i/m16a4
$execute if score #random {ns}.data matches 2 run loot replace entity @s $(slot) loot {ns}:i/m16a4
$execute if score #random {ns}.data matches 3 run loot replace entity @s $(slot) loot {ns}:i/ak47
$execute if score #random {ns}.data matches 4 run loot replace entity @s $(slot) loot {ns}:i/fnfal
$execute if score #random {ns}.data matches 5 run loot replace entity @s $(slot) loot {ns}:i/aug
$execute if score #random {ns}.data matches 6 run loot replace entity @s $(slot) loot {ns}:i/m4a1
$execute if score #random {ns}.data matches 7 run loot replace entity @s $(slot) loot {ns}:i/g3a3
$execute if score #random {ns}.data matches 8 run loot replace entity @s $(slot) loot {ns}:i/famas
$execute if score #random {ns}.data matches 9 run loot replace entity @s $(slot) loot {ns}:i/scar17
$execute if score #random {ns}.data matches 10 run loot replace entity @s $(slot) loot {ns}:i/m1911
$execute if score #random {ns}.data matches 11 run loot replace entity @s $(slot) loot {ns}:i/m9
$execute if score #random {ns}.data matches 12 run loot replace entity @s $(slot) loot {ns}:i/deagle
$execute if score #random {ns}.data matches 13 run loot replace entity @s $(slot) loot {ns}:i/makarov
$execute if score #random {ns}.data matches 14 run loot replace entity @s $(slot) loot {ns}:i/glock17
$execute if score #random {ns}.data matches 15 run loot replace entity @s $(slot) loot {ns}:i/glock18
$execute if score #random {ns}.data matches 16 run loot replace entity @s $(slot) loot {ns}:i/vz61
$execute if score #random {ns}.data matches 17 run loot replace entity @s $(slot) loot {ns}:i/mp5
$execute if score #random {ns}.data matches 18 run loot replace entity @s $(slot) loot {ns}:i/mac10
$execute if score #random {ns}.data matches 19 run loot replace entity @s $(slot) loot {ns}:i/mp7
$execute if score #random {ns}.data matches 20 run loot replace entity @s $(slot) loot {ns}:i/ppsh41
$execute if score #random {ns}.data matches 21 run loot replace entity @s $(slot) loot {ns}:i/sten
$execute if score #random {ns}.data matches 22 run loot replace entity @s $(slot) loot {ns}:i/spas12
$execute if score #random {ns}.data matches 23 run loot replace entity @s $(slot) loot {ns}:i/m500
$execute if score #random {ns}.data matches 24 run loot replace entity @s $(slot) loot {ns}:i/m590
$execute if score #random {ns}.data matches 25 run loot replace entity @s $(slot) loot {ns}:i/svd
$execute if score #random {ns}.data matches 26 run loot replace entity @s $(slot) loot {ns}:i/m82
$execute if score #random {ns}.data matches 27 run loot replace entity @s $(slot) loot {ns}:i/mosin
$execute if score #random {ns}.data matches 28 run loot replace entity @s $(slot) loot {ns}:i/m24
$execute if score #random {ns}.data matches 29 run loot replace entity @s $(slot) loot {ns}:i/rpg7
$execute if score #random {ns}.data matches 30 run loot replace entity @s $(slot) loot {ns}:i/rpk
$execute if score #random {ns}.data matches 31 run loot replace entity @s $(slot) loot {ns}:i/m249
""")

