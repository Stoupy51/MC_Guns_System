
# Imports
from stewbeet import Context, official_lib_used

from .functional.main import main as main_datapack
from .functional.map_editor import generate_map_editor
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

    # Zombies functional initialization
    main_zombies()

    # Multiplayer functional initialization
    main_multiplayer()

    # Map editor (generic for multiplayer, zombies, missions)
    generate_map_editor()

    # Bookshelf dump module
    official_lib_used("bs.dump")

