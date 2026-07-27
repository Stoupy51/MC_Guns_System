""" Item modifiers for the grenade stack and the white-pixel font behind the flash overlay. """
# Imports
from beet import Font, Texture
from PIL import Image
from stewbeet import ItemModifier, Mem, set_json_encoder


# Functions
def write_grenade_setup() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Create item modifier to consume one grenade from the stack
	Mem.ctx.data[ns].item_modifiers[f"v{version}/grenade/consume_one"] = set_json_encoder(
		ItemModifier({"function": "minecraft:set_count", "count": -1, "add": True}),
		max_level=-1
	)

	# Create item modifiers to set grenade count (for initial give and replenishment)
	for i in (4, 3, 2):
		Mem.ctx.data[ns].item_modifiers[f"v{version}/grenade/set_count_{i}"] = set_json_encoder(
			ItemModifier({"function": "minecraft:set_count", "count": i}),
			max_level=-1
		)
	Mem.ctx.data[ns].item_modifiers[f"v{version}/grenade/set_count_add_2"] = set_json_encoder(
		ItemModifier({"function": "minecraft:set_count", "count": 2, "add": True}),
		max_level=-1
	)

	# Create white pixel texture for flash grenade screen fill
	white_pixel = Image.new("RGB", (1, 1), (255, 255, 255))
	Mem.ctx.assets.textures[f"{ns}:font/flash_white"] = Texture(white_pixel)

	# Add font provider for flash screen (1x1 white pixel scaled to fill the screen)
	flash_font: Font = Mem.ctx.assets.fonts.setdefault(f"{ns}:flash", Font({"providers": []}))
	flash_font.data["providers"].append({
		"type": "bitmap",
		"file": f"{ns}:font/flash_white.png",
		"ascent": 4000,
		"height": 8000,
		"chars": ["F"]
	})

