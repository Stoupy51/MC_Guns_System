""" Footstep and impact sound groups. """
# Imports
from stewbeet import Mem, write_tag


# Functions
def write_sound_tags() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Write block sounds tags
	write_tag(f"{ns}:v{version}/sounds/cloth", Mem.ctx.data.block_tags, values=[
		"#minecraft:wool",
		"minecraft:target",
		"minecraft:hay_block",
		"minecraft:sponge",
		"minecraft:snow_block",
		"minecraft:powder_snow",
		"minecraft:tnt",
		"minecraft:moss_block",
		"minecraft:bell",
		"minecraft:dried_kelp_block"
	])
	write_tag(f"{ns}:v{version}/sounds/dirt", Mem.ctx.data.block_tags, values=[
		f"#{ns}:v{version}/dirt",
		f"#{ns}:v{version}/concrete_powder",
		"minecraft:nether_quartz_ore",
		"minecraft:nether_gold_ore",
		"minecraft:pointed_dripstone"
	])
	write_tag(f"{ns}:v{version}/sounds/glass", Mem.ctx.data.block_tags, values=[
		"#minecraft:ice",
		f"#{ns}:v{version}/stained_glass_pane",
		"minecraft:tinted_glass",
		"minecraft:white_stained_glass",
		"minecraft:orange_stained_glass",
		"minecraft:magenta_stained_glass",
		"minecraft:light_blue_stained_glass",
		"minecraft:yellow_stained_glass",
		"minecraft:lime_stained_glass",
		"minecraft:pink_stained_glass",
		"minecraft:gray_stained_glass",
		"minecraft:light_gray_stained_glass",
		"minecraft:cyan_stained_glass",
		"minecraft:purple_stained_glass",
		"minecraft:blue_stained_glass",
		"minecraft:brown_stained_glass",
		"minecraft:green_stained_glass",
		"minecraft:red_stained_glass",
		"minecraft:black_stained_glass",
		"minecraft:glass",
		"minecraft:glass_pane",
		"minecraft:beacon",
		"minecraft:glowstone",
		"minecraft:redstone_lamp",
		"minecraft:sea_lantern",
		"minecraft:amethyst_cluster"
	])
	write_tag(f"{ns}:v{version}/sounds/mud", Mem.ctx.data.block_tags, values=[
		f"#{ns}:v{version}/mud",
		"minecraft:slime_block",
		"minecraft:honey_block",
		"minecraft:melon",
		"minecraft:wet_sponge",
		"minecraft:pumpkin",
		"minecraft:carved_pumpkin",
		"minecraft:jack_o_lantern",
		"minecraft:nether_wart_block",
		"minecraft:warped_wart_block",
		"minecraft:shroomlight",
		"minecraft:honeycomb_block",
		"minecraft:lava",
		"minecraft:cactus",
		"minecraft:bee_nest",
		"minecraft:sculk_sensor",
		"minecraft:ochre_froglight",
		"minecraft:pearlescent_froglight",
		"minecraft:verdant_froglight",
		"minecraft:sculk"
	])
	write_tag(f"{ns}:v{version}/sounds/special_sound", Mem.ctx.data.block_tags, values=[
		f"#{ns}:v{version}/sounds/glass",
		f"#{ns}:v{version}/sounds/water",
		f"#{ns}:v{version}/sounds/cloth",
		f"#{ns}:v{version}/sounds/dirt",
		f"#{ns}:v{version}/sounds/mud",
		f"#{ns}:v{version}/sounds/wood"
	])
	write_tag(f"{ns}:v{version}/sounds/water", Mem.ctx.data.block_tags, values=[
		"minecraft:water",
		"minecraft:kelp_plant",
		"minecraft:tall_seagrass",
		"minecraft:seagrass",
		"minecraft:bubble_column"
	])
	write_tag(f"{ns}:v{version}/sounds/wood", Mem.ctx.data.block_tags, values=[
		"#minecraft:logs",
		"#minecraft:planks",
		"#minecraft:bamboo_blocks",
		"minecraft:bone_block",
		"minecraft:note_block",
		"minecraft:jukebox",
		"minecraft:bookshelf",
		"minecraft:mangrove_roots",
		"minecraft:bamboo_mosaic",
		"minecraft:chiseled_bookshelf"
	])

