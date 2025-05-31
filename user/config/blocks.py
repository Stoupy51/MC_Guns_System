
# Imports
from python_datapack.utils.io import *


# Main function
def main(config: dict) -> None:
    version: str = config["version"]
    ns: str = config["namespace"]

    # Write empty block tag
    write_tags(config, f"{ns}:block/v{version}/empty", stp.super_json_dump({"values": []}))

    # Write block tags
    write_tags(config, f"{ns}:block/v{version}/air", stp.super_json_dump({
        "values": [
            "#minecraft:banners",
            "#minecraft:buttons",
            "#minecraft:wool_carpets",
            "#minecraft:corals",
            "#minecraft:wooden_doors",
            "#minecraft:flower_pots",
            "#minecraft:beds",
            "#minecraft:leaves",
            "#minecraft:rails",
            "#minecraft:wooden_pressure_plates",
            "#minecraft:wooden_trapdoors",
            "#minecraft:signs",
            "#minecraft:fences",
            "#minecraft:candle_cakes",
            "#minecraft:candles",
            "minecraft:air",
            "minecraft:cave_air",
            "minecraft:void_air",
            "minecraft:light",
            "minecraft:structure_void",
            f"#{ns}:v{version}/plant",
            f"#{ns}:v{version}/fence_gate",
            f"#{ns}:v{version}/stained_glass_pane",
            "minecraft:cobweb",
            "minecraft:torch",
            "minecraft:wall_torch",
            "minecraft:end_rod",
            "minecraft:ladder",
            "minecraft:snow",
            "minecraft:cake",
            "minecraft:iron_bars",
            "minecraft:glass_pane",
            "minecraft:lever",
            "minecraft:stone_pressure_plate",
            "minecraft:light_weighted_pressure_plate",
            "minecraft:heavy_weighted_pressure_plate",
            "minecraft:repeater",
            "minecraft:comparator",
            "minecraft:redstone_wire",
            "minecraft:redstone_torch",
            "minecraft:redstone_wall_torch",
            "minecraft:tripwire_hook",
            "minecraft:conduit",
            "minecraft:turtle_egg",
            "minecraft:fire",
            "minecraft:barrier",
            "minecraft:cocoa",
            "minecraft:lantern",
            "minecraft:soul_lantern",
            "minecraft:scaffolding",
            "minecraft:tripwire",
            "minecraft:chain",
            "minecraft:small_amethyst_bud",
            "minecraft:medium_amethyst_bud",
            "minecraft:large_amethyst_bud",
            "minecraft:lightning_rod",
            "minecraft:frogspawn",
            "minecraft:sculk_vein",
            "minecraft:nether_portal",
            "minecraft:end_portal"
        ]
    }))

    write_tags(config, f"{ns}:block/v{version}/solid", stp.super_json_dump({
        "values": [
            "#minecraft:wool",
            "#minecraft:anvil",
            "#minecraft:coral_blocks",
            "#minecraft:logs",
            "#minecraft:planks",
            "#minecraft:bamboo_blocks",
            f"#{ns}:v{version}/concrete",
            f"#{ns}:v{version}/concrete_powder",
            f"#{ns}:v{version}/terracotta",
            f"#{ns}:v{version}/stones",
            f"#{ns}:v{version}/ores",
            f"#{ns}:v{version}/dirt",
            f"#{ns}:v{version}/mud",
            f"#{ns}:v{version}/misc"
        ]
    }))

    write_tags(config, f"{ns}:block/v{version}/plant", stp.super_json_dump({
        "values": [
            "#minecraft:crops",
            "#minecraft:flowers",
            "#minecraft:saplings",
            "#minecraft:flowers",
            "#minecraft:cave_vines",
            "#minecraft:replaceable",
            "#minecraft:leaves",
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
            "minecraft:twisting_vines",
            "minecraft:twisting_vines_plant",
            "minecraft:weeping_vines",
            "minecraft:weeping_vines_plant",
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
            "minecraft:nether_sprouts"
        ]
    }))

    write_tags(config, f"{ns}:block/v{version}/misc", stp.super_json_dump({
        "values": [
            "#minecraft:dragon_immune",
            "#minecraft:beacon_base_blocks",
            "#minecraft:campfires",
            "#minecraft:climbable",
            "#minecraft:infiniburn_overworld",
            "#minecraft:gold_ores",
            "#minecraft:iron_ores",
            "minecraft:netherrack",
            "minecraft:soul_sand",
            "minecraft:soul_soil",
            "minecraft:spawner",
            "minecraft:crying_obsidian",
            "minecraft:end_stone",
            "minecraft:chorus_plant",
            "minecraft:chorus_flower",
            "minecraft:crafting_table",
            "minecraft:enchanting_table",
            "minecraft:brewing_stand",
            "minecraft:chest",
            "minecraft:ender_chest",
            "minecraft:piston",
            "minecraft:sticky_piston",
            "minecraft:dispenser",
            "minecraft:dropper",
            "minecraft:hopper",
            "minecraft:grindstone",
            "minecraft:lectern",
            "minecraft:respawn_anchor",
            "minecraft:smoker"
        ]
    }))

    write_tags(config, f"{ns}:block/v{version}/dirt", stp.super_json_dump({
        "values": [
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
            "minecraft:soul_soil",
            "minecraft:crimson_nylium",
            "minecraft:warped_nylium",
            "minecraft:sculk_catalyst"
        ]
    }))

    write_tags(config, f"{ns}:block/v{version}/activate", stp.super_json_dump({
        "values": [
            "minecraft:lever",
            "minecraft:stone_button",
            "minecraft:polished_blackstone_button"
        ]
    }))

    write_tags(config, f"{ns}:block/v{version}/terracotta", stp.super_json_dump({
        "values": [
            "minecraft:terracotta",
            "minecraft:white_terracotta",
            "minecraft:orange_terracotta",
            "minecraft:magenta_terracotta",
            "minecraft:light_blue_terracotta",
            "minecraft:yellow_terracotta",
            "minecraft:lime_terracotta",
            "minecraft:pink_terracotta",
            "minecraft:gray_terracotta",
            "minecraft:light_gray_terracotta",
            "minecraft:cyan_terracotta",
            "minecraft:purple_terracotta",
            "minecraft:blue_terracotta",
            "minecraft:brown_terracotta",
            "minecraft:green_terracotta",
            "minecraft:red_terracotta",
            "minecraft:black_terracotta",
            "minecraft:bricks",
            "minecraft:brick_slab",
            "minecraft:brick_stairs",
            "minecraft:brick_wall",
            "minecraft:nether_bricks",
            "minecraft:cracked_nether_bricks",
            "minecraft:nether_brick_slab",
            "minecraft:nether_brick_stairs",
            "minecraft:nether_brick_wall",
            "minecraft:nether_brick_fence",
            "minecraft:red_nether_bricks",
            "minecraft:red_nether_brick_slab",
            "minecraft:red_nether_brick_stairs",
            "minecraft:red_nether_brick_wall",
            "minecraft:end_stone_bricks",
            "minecraft:end_stone_brick_slab",
            "minecraft:end_stone_brick_stairs",
            "minecraft:end_stone_brick_wall",
            "minecraft:prismarine_bricks",
            "minecraft:prismarine_brick_slab",
            "minecraft:prismarine_brick_stairs"
        ]
    }))

    write_tags(config, f"{ns}:block/v{version}/stones", stp.super_json_dump({
        "values": [
            "#minecraft:stone_bricks",
            "#minecraft:deepslate_ore_replaceables",
            "#minecraft:base_stone_overworld",
            "#minecraft:base_stone_nether",
            "minecraft:stone",
            "minecraft:stone_slab",
            "minecraft:stone_stairs",
            "minecraft:cobblestone",
            "minecraft:cobblestone_slab",
            "minecraft:cobblestone_stairs",
            "minecraft:cobblestone_wall",
            "minecraft:mossy_cobblestone",
            "minecraft:mossy_cobblestone_slab",
            "minecraft:mossy_cobblestone_stairs",
            "minecraft:mossy_cobblestone_wall",
            "minecraft:diorite",
            "minecraft:diorite_slab",
            "minecraft:diorite_stairs",
            "minecraft:diorite_wall",
            "minecraft:polished_diorite",
            "minecraft:polished_diorite_slab",
            "minecraft:polished_diorite_stairs",
            "minecraft:granite",
            "minecraft:granite_slab",
            "minecraft:granite_stairs",
            "minecraft:granite_wall",
            "minecraft:polished_granite",
            "minecraft:polished_granite_slab",
            "minecraft:polished_granite_stairs",
            "minecraft:andesite",
            "minecraft:andesite_slab",
            "minecraft:andesite_stairs",
            "minecraft:andesite_wall",
            "minecraft:polished_andesite",
            "minecraft:polished_andesite_slab",
            "minecraft:polished_andesite_stairs",
            "minecraft:deepslate",
            "minecraft:deepslate_tiles",
            "minecraft:cracked_deepslate_tiles",
            "minecraft:deepslate_tile_slab",
            "minecraft:deepslate_tile_stairs",
            "minecraft:deepslate_tile_wall",
            "minecraft:deepslate_bricks",
            "minecraft:cracked_deepslate_bricks",
            "minecraft:deepslate_brick_slab",
            "minecraft:deepslate_brick_stairs",
            "minecraft:deepslate_brick_wall",
            "minecraft:chiseled_deepslate",
            "minecraft:cobbled_deepslate",
            "minecraft:cobbled_deepslate_slab",
            "minecraft:cobbled_deepslate_stairs",
            "minecraft:cobbled_deepslate_wall",
            "minecraft:polished_deepslate",
            "minecraft:polished_deepslate_slab",
            "minecraft:polished_deepslate_stairs",
            "minecraft:polished_deepslate_wall",
            "minecraft:blackstone",
            "minecraft:blackstone_slab",
            "minecraft:blackstone_stairs",
            "minecraft:blackstone_wall",
            "minecraft:polished_blackstone",
            "minecraft:polished_blackstone_slab",
            "minecraft:polished_blackstone_stairs",
            "minecraft:polished_blackstone_wall",
            "minecraft:polished_blackstone_bricks",
            "minecraft:cracked_polished_blackstone_bricks",
            "minecraft:polished_blackstone_brick_slab",
            "minecraft:polished_blackstone_brick_stairs",
            "minecraft:polished_blackstone_brick_wall"
        ]
    }))

    write_tags(config, f"{ns}:block/v{version}/stained_glass_pane", stp.super_json_dump({
        "values": [
            "minecraft:white_stained_glass_pane",
            "minecraft:orange_stained_glass_pane",
            "minecraft:magenta_stained_glass_pane",
            "minecraft:light_blue_stained_glass_pane",
            "minecraft:yellow_stained_glass_pane",
            "minecraft:lime_stained_glass_pane",
            "minecraft:pink_stained_glass_pane",
            "minecraft:gray_stained_glass_pane",
            "minecraft:light_gray_stained_glass_pane",
            "minecraft:cyan_stained_glass_pane",
            "minecraft:purple_stained_glass_pane",
            "minecraft:blue_stained_glass_pane",
            "minecraft:brown_stained_glass_pane",
            "minecraft:green_stained_glass_pane",
            "minecraft:red_stained_glass_pane",
            "minecraft:black_stained_glass_pane",
            "minecraft:glass_pane",
            "minecraft:iron_bars"
        ]
    }))

    write_tags(config, f"{ns}:block/v{version}/outside", stp.super_json_dump({
        "values": [
            "#minecraft:crops",
            "#minecraft:flowers",
            "#minecraft:saplings",
            "#minecraft:replaceable",
            "#minecraft:bamboo_plantable_on",
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
        ]
    }))

    write_tags(config, f"{ns}:block/v{version}/ores", stp.super_json_dump({
        "values": [
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
        ]
    }))

    write_tags(config, f"{ns}:block/v{version}/mud", stp.super_json_dump({
        "values": [
            "minecraft:mud",
            "minecraft:packed_mud",
            "minecraft:mud_bricks"
        ]
    }))

    write_tags(config, f"{ns}:block/v{version}/jump", stp.super_json_dump({
        "values": [
            "minecraft:slime_block",
            "minecraft:honey_block",
            "minecraft:hay_block"
        ]
    }))

    write_tags(config, f"{ns}:block/v{version}/fence_gate", stp.super_json_dump({
        "values": [
            "minecraft:acacia_fence_gate",
            "minecraft:birch_fence_gate",
            "minecraft:dark_oak_fence_gate",
            "minecraft:jungle_fence_gate",
            "minecraft:oak_fence_gate",
            "minecraft:spruce_fence_gate",
            "minecraft:warped_fence_gate",
            "minecraft:crimson_fence_gate"
        ]
    }))

    write_tags(config, f"{ns}:block/v{version}/concrete_powder", stp.super_json_dump({
        "values": [
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
        ]
    }))

    write_tags(config, f"{ns}:block/v{version}/concrete", stp.super_json_dump({
        "values": [
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
        ]
    }))

    # Write block sounds tags
    write_tags(config, f"{ns}:block/v{version}/sounds/cloth", stp.super_json_dump({
        "values": [
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
        ]
    }))
    write_tags(config, f"{ns}:block/v{version}/sounds/dirt", stp.super_json_dump({
        "values": [
            f"#{ns}:v{version}/dirt",
            f"#{ns}:v{version}/concrete_powder",
            "minecraft:nether_quartz_ore",
            "minecraft:nether_gold_ore",
            "minecraft:pointed_dripstone"
        ]
    }))
    write_tags(config, f"{ns}:block/v{version}/sounds/glass", stp.super_json_dump({
        "values": [
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
        ]
    }))
    write_tags(config, f"{ns}:block/v{version}/sounds/mud", stp.super_json_dump({
        "values": [
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
        ]
    }))
    write_tags(config, f"{ns}:block/v{version}/sounds/special_sound", stp.super_json_dump({
        "values": [
            f"#{ns}:v{version}/sounds/glass",
            f"#{ns}:v{version}/sounds/water",
            f"#{ns}:v{version}/sounds/cloth",
            f"#{ns}:v{version}/sounds/dirt",
            f"#{ns}:v{version}/sounds/mud",
            f"#{ns}:v{version}/sounds/wood"
        ]
    }))
    write_tags(config, f"{ns}:block/v{version}/sounds/water", stp.super_json_dump({
        "values": [
            "minecraft:water",
            "minecraft:kelp_plant",
            "minecraft:tall_seagrass",
            "minecraft:seagrass",
            "minecraft:bubble_column"
        ]
    }))
    write_tags(config, f"{ns}:block/v{version}/sounds/wood", stp.super_json_dump({
        "values": [
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
        ]
    }))

