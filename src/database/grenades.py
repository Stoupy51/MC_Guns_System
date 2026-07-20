
# Imports
from ..config.stats import FLASH_GRENADE, FRAG_GRENADE, MONKEY_BOMB, SEMTEX, SMOKE_GRENADE, add_item


# Main function should return a database
def main() -> None:

    # Add grenades
    add_item("frag_grenade", stats=FRAG_GRENADE, model_path="auto", max_stack_size=4)
    add_item("semtex", stats=SEMTEX, model_path="auto", max_stack_size=4)
    add_item("smoke_grenade", stats=SMOKE_GRENADE, model_path="auto", max_stack_size=4)
    add_item("flash_grenade", stats=FLASH_GRENADE, model_path="auto", max_stack_size=4)

    # Zombies-exclusive tactical (mystery box / wallbuys only, never in MP loadouts): capped at 3
    # by the give/refill functions (zombies/wallbuys/give_tactical + bonus/max_ammo_grenades)
    add_item("monkey_bomb", stats=MONKEY_BOMB, model_path="auto", max_stack_size=3)

