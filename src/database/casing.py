
# Imports
from stewbeet import Item

from ..config.stats import (
    CASING_9X18MM,
    CASING_9X19MM,
    CASING_12GA3IN,
    CASING_12GA275IN,
    CASING_32ACP,
    CASING_45ACP,
    CASING_46X30MM,
    CASING_50AE,
    CASING_50BMG,
    CASING_338LAPUA,
    CASING_556X45MM,
    CASING_762X25MM,
    CASING_762X39MM,
    CASING_762X51MM,
    CASING_762X54MM,
    add_item,
)


# Main function should return a database
def main() -> None:

    # Add casings
    casings: list[Item] = [
        add_item(x, model_path="auto")
        for x in (
            CASING_9X18MM, CASING_9X19MM, CASING_12GA3IN, CASING_12GA275IN, CASING_32ACP,
            CASING_45ACP, CASING_46X30MM, CASING_50AE, CASING_50BMG, CASING_338LAPUA,
            CASING_556X45MM, CASING_762X25MM, CASING_762X39MM, CASING_762X51MM,
            CASING_762X54MM,
        )
    ]

    # Define names as their ID
    for obj in casings:
        obj.components["item_name"] = {"text": obj.id, "color": "white"}

