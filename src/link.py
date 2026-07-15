
# Imports
from stewbeet import Context, official_lib_used

from .functional.core import main as main_core
from .functional.main import main as main_datapack
from .functional.map_editor import generate_map_editor
from .functional.missions import main as main_missions
from .functional.mob_ai import main as main_mob_ai
from .functional.multiplayer import main as main_multiplayer
from .functional.player_config import main as main_player_config
from .functional.shaders import main as main_shaders
from .functional.stamina import main as main_stamina
from .functional.weapon import main as main_weapon
from .functional.zombies import main as main_zombies


# Main function is run just before making finalyzing the build process (zip, headers, lang, ...)
def beet_default(ctx: Context) -> None:
    ns: str = ctx.project_id

    main_datapack()
    main_shaders()
    main_weapon()
    main_player_config()
    main_stamina()
    main_mob_ai()

    # Shared core functions (bounds, teleport, maps, commands, spawning)
    main_core()

    # Zombies functional initialization
    main_zombies()

    # Multiplayer functional initialization
    main_multiplayer()

    # Missions functional initialization
    main_missions()

    # Map editor (generic for multiplayer, zombies, missions)
    generate_map_editor()

    # Bookshelf dump module
    official_lib_used("bs.dump")

    # Generate 3D renders (excluding _zoom variants)
    from stewbeet import Item, Mem
    from stewbeet.plugins.ingame_manual.config import ManualConfig  # pyright: ignore[reportMissingTypeStubs]
    from stewbeet.plugins.ingame_manual.iso_renders import generate_all_iso_renders  # pyright: ignore[reportMissingTypeStubs]
    [Item.from_id(x).components.pop("item_model", None) for x in Mem.definitions.keys() if x.endswith("_zoom")]
    config = ManualConfig(
        project_id=ctx.project_id,
        project_name=ctx.project_name,
        project_author=ctx.project_author,
        cache_path=f"{Mem.ctx.directory}/manual_cache",
    )
    iso_renders_cache: str = f"{Mem.ctx.directory}/iso_renders"
    generate_all_iso_renders(config, override_cache_path=f"{iso_renders_cache}/items", ignore_vanilla=True, ignore_painting=True)

    # Generate all_items.png showcase grid, excluding _zoom/_empty variants (which have no iso render, see above).
    # Reads renders from "{iso_renders_cache}/items/{project_id}" and saves to the output directory.
    from PIL import Image
    from stewbeet.plugins.ingame_manual.paths import template_path  # pyright: ignore[reportMissingTypeStubs]
    from stewbeet.plugins.ingame_manual.showcase import generate_showcase_images  # pyright: ignore[reportMissingTypeStubs]
    simple_case: Image.Image = Image.open(template_path("simple_case_no_border.png"))
    showcase_items: list[str] = [
        x for x in Mem.definitions.keys()
        if not x.endswith(("_zoom", "_empty")) and Item.from_id(x).components.get("item_model", "").startswith(f"{ns}:")
    ]
    generate_showcase_images(2, {}, simple_case, iso_renders_cache, all_items=showcase_items)

