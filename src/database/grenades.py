
# Imports
from ..config.stats import FLASH_GRENADE, FRAG_GRENADE, SEMTEX, SMOKE_GRENADE, add_item


# Main function should return a database
def main() -> None:

    # Add grenades
    add_item("frag_grenade", stats=FRAG_GRENADE, model_path="auto")
    add_item("semtex", stats=SEMTEX, model_path="auto")
    add_item("smoke_grenade", stats=SMOKE_GRENADE, model_path="auto")
    add_item("flash_grenade", stats=FLASH_GRENADE, model_path="auto")
