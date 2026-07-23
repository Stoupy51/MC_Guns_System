
# Imports
from stewbeet import Mem

from ..config.stats import FLASH_GRENADE, FRAG_GRENADE, MONKEY_BOMB, SEMTEX, SMOKE_GRENADE, WEB_GRENADE, add_item, get_model_path


# Main function should return a database
def main() -> None:
    ns: str = Mem.ctx.project_id

    # Add grenades
    add_item("frag_grenade", stats=FRAG_GRENADE, model_path="auto", max_stack_size=4)
    add_item("semtex", stats=SEMTEX, model_path="auto", max_stack_size=4)
    add_item("smoke_grenade", stats=SMOKE_GRENADE, model_path="auto", max_stack_size=4)
    add_item("flash_grenade", stats=FLASH_GRENADE, model_path="auto", max_stack_size=4)

    # Widow's Wine web grenade (perk-exclusive)
    web = add_item("web_grenade", stats=WEB_GRENADE, model_path=get_model_path("frag_grenade"), max_stack_size=4)
    if web.override_model:
        for k in web.override_model["textures"].keys():
            web.override_model["textures"][k] = f"{ns}:item/cobweb"

    # Zombies-exclusive tactical (mystery box / wallbuys only, never in MP loadouts): capped at 3
    # by the give/refill functions (zombies/wallbuys/give_tactical + bonus/max_ammo_grenades)
    add_item("monkey_bomb", stats=MONKEY_BOMB, model_path="auto", max_stack_size=3)

