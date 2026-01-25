
# Imports
from stewbeet import Context

from .functional.main import main as main_datapack
from .functional.multiplayer import main as main_multiplayer
from .functional.shaders import main as main_shaders
from .functional.tick import main as main_tick
from .functional.weapon import main as main_weapon


# Main function is run just before making finalyzing the build process (zip, headers, lang, ...)
def beet_default(ctx: Context) -> None:
    main_datapack()
    main_shaders()
    main_weapon()
    main_tick()

    # Multiplayer functional initialization
    main_multiplayer()

