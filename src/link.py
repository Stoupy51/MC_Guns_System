
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
from .functional.tick import main as main_tick
from .functional.weapon import main as main_weapon
from .functional.zombies import main as main_zombies


# Main function is run just before making finalyzing the build process (zip, headers, lang, ...)
def beet_default(ctx: Context) -> None:
    main_datapack()
    main_shaders()
    main_weapon()
    main_player_config()
    main_mob_ai()
    main_tick()

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
    from stewbeet.plugins.ingame_manual.iso_renders import generate_all_iso_renders  # pyright: ignore[reportMissingTypeStubs]
    [Item.from_id(x).components.pop("item_model", None) for x in Mem.definitions.keys() if x.endswith("_zoom")]
    generate_all_iso_renders(override_cache_path=f"{Mem.ctx.directory}/iso_renders", ignore_vanilla=True, ignore_painting=True)

