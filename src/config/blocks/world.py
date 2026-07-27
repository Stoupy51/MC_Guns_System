""" World tags: outside blocks, ores, mud, jump pads, fence gates and concrete. """
# Imports
from stewbeet import Mem, write_tag


# Functions
def write_world_tags() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_tag(f"{ns}:v{version}/outside", Mem.ctx.data.block_tags, values=[
		"#minecraft:crops",
		"#minecraft:flowers",
		"#minecraft:saplings",
		"#minecraft:replaceable",
		"#minecraft:supports_bamboo",
		"minecraft:short_grass",
		"minecraft:tall_grass",
		"minecraft:seagrass",
		"minecraft:tall_seagrass",
		"minecraft:fern",
		"minecraft:large_fern",
		"minecraft:kelp",
		"minecraft:kelp_plant",
		"minecraft:lily_pad",
		"minecraft:sugar_cane",
		"minecraft:vine",
		"minecraft:glow_lichen",
		"minecraft:hanging_roots",
		"minecraft:spore_blossom",
		"minecraft:moss_carpet",
		"minecraft:bamboo",
		"minecraft:bamboo_sapling",
		"minecraft:azalea",
		"minecraft:flowering_azalea",
		"minecraft:dead_bush",
		"minecraft:small_dripleaf",
		"minecraft:big_dripleaf",
		"minecraft:big_dripleaf_stem",
		"minecraft:crimson_fungus",
		"minecraft:warped_fungus",
		"minecraft:crimson_roots",
		"minecraft:warped_roots",
		"minecraft:nether_sprouts",
		"#minecraft:dirt",
		"#minecraft:sand",
		"minecraft:gravel",
		"minecraft:clay",
		"minecraft:farmland",
		"minecraft:dirt_path",
		"minecraft:podzol",
		"minecraft:mycelium",
		"minecraft:rooted_dirt",
		"minecraft:mud",
		"minecraft:muddy_mangrove_roots",
		"minecraft:packed_mud",
		"minecraft:suspicious_sand",
		"minecraft:suspicious_gravel",
		"minecraft:soul_sand",
		"minecraft:soul_soil"
	])

	write_tag(f"{ns}:v{version}/ores", Mem.ctx.data.block_tags, values=[
		"#minecraft:coal_ores",
		"#minecraft:copper_ores",
		"#minecraft:diamond_ores",
		"#minecraft:emerald_ores",
		"#minecraft:gold_ores",
		"#minecraft:iron_ores",
		"#minecraft:lapis_ores",
		"#minecraft:redstone_ores",
		"minecraft:ancient_debris",
		"minecraft:nether_gold_ore",
		"minecraft:nether_quartz_ore",
		"minecraft:raw_copper_block",
		"minecraft:raw_gold_block",
		"minecraft:raw_iron_block",
		"minecraft:copper_block",
		"minecraft:exposed_copper",
		"minecraft:weathered_copper",
		"minecraft:oxidized_copper",
		"minecraft:cut_copper",
		"minecraft:exposed_cut_copper",
		"minecraft:weathered_cut_copper",
		"minecraft:oxidized_cut_copper",
		"minecraft:cut_copper_slab",
		"minecraft:exposed_cut_copper_slab",
		"minecraft:weathered_cut_copper_slab",
		"minecraft:oxidized_cut_copper_slab",
		"minecraft:cut_copper_stairs",
		"minecraft:exposed_cut_copper_stairs",
		"minecraft:weathered_cut_copper_stairs",
		"minecraft:oxidized_cut_copper_stairs",
		"minecraft:waxed_copper_block",
		"minecraft:waxed_exposed_copper",
		"minecraft:waxed_weathered_copper",
		"minecraft:waxed_oxidized_copper",
		"minecraft:waxed_cut_copper",
		"minecraft:waxed_exposed_cut_copper",
		"minecraft:waxed_weathered_cut_copper",
		"minecraft:waxed_oxidized_cut_copper",
		"minecraft:waxed_cut_copper_slab",
		"minecraft:waxed_exposed_cut_copper_slab",
		"minecraft:waxed_weathered_cut_copper_slab",
		"minecraft:waxed_oxidized_cut_copper_slab",
		"minecraft:waxed_cut_copper_stairs",
		"minecraft:waxed_exposed_cut_copper_stairs",
		"minecraft:waxed_weathered_cut_copper_stairs",
		"minecraft:waxed_oxidized_cut_copper_stairs"
	])

	write_tag(f"{ns}:v{version}/mud", Mem.ctx.data.block_tags, values=[
		"minecraft:mud",
		"minecraft:packed_mud",
		"minecraft:mud_bricks"
	])

	write_tag(f"{ns}:v{version}/jump", Mem.ctx.data.block_tags, values=[
		"minecraft:slime_block",
		"minecraft:honey_block",
		"minecraft:hay_block"
	])

	write_tag(f"{ns}:v{version}/fence_gate", Mem.ctx.data.block_tags, values=[
		"minecraft:acacia_fence_gate",
		"minecraft:birch_fence_gate",
		"minecraft:dark_oak_fence_gate",
		"minecraft:jungle_fence_gate",
		"minecraft:oak_fence_gate",
		"minecraft:spruce_fence_gate",
		"minecraft:warped_fence_gate",
		"minecraft:crimson_fence_gate"
	])

	write_tag(f"{ns}:v{version}/concrete_powder", Mem.ctx.data.block_tags, values=[
		"minecraft:white_concrete_powder",
		"minecraft:orange_concrete_powder",
		"minecraft:magenta_concrete_powder",
		"minecraft:light_blue_concrete_powder",
		"minecraft:yellow_concrete_powder",
		"minecraft:lime_concrete_powder",
		"minecraft:pink_concrete_powder",
		"minecraft:gray_concrete_powder",
		"minecraft:light_gray_concrete_powder",
		"minecraft:cyan_concrete_powder",
		"minecraft:purple_concrete_powder",
		"minecraft:blue_concrete_powder",
		"minecraft:brown_concrete_powder",
		"minecraft:green_concrete_powder",
		"minecraft:red_concrete_powder",
		"minecraft:black_concrete_powder"
	])

	write_tag(f"{ns}:v{version}/concrete", Mem.ctx.data.block_tags, values=[
		"minecraft:white_concrete",
		"minecraft:orange_concrete",
		"minecraft:magenta_concrete",
		"minecraft:light_blue_concrete",
		"minecraft:yellow_concrete",
		"minecraft:lime_concrete",
		"minecraft:pink_concrete",
		"minecraft:gray_concrete",
		"minecraft:light_gray_concrete",
		"minecraft:cyan_concrete",
		"minecraft:purple_concrete",
		"minecraft:blue_concrete",
		"minecraft:brown_concrete",
		"minecraft:green_concrete",
		"minecraft:red_concrete",
		"minecraft:black_concrete"
	])

