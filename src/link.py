
# Imports
from stewbeet import Context, Mem

from .functional.main import main as main_datapack
from .functional.tick import main as main_tick
from .functional.weapon import main as main_weapon


# Main function is run just before making finalyzing the build process (zip, headers, lang, ...)
def beet_default(ctx: Context) -> None:
    if Mem.ctx is None:
        Mem.ctx = ctx
    main_datapack()
    main_weapon()
    main_tick()

