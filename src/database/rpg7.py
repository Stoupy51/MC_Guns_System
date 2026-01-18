
# Imports
from ..config.stats import RPG7, add_item


# Main function should return a database
def main() -> None:

    # Add rpg7
    add_item("rpg7", stats=RPG7, model_path="auto")
    add_item("rpg7_zoom", stats=RPG7, model_path="auto")
    add_item("rpg7_empty", stats=RPG7, model_path="auto")
    add_item("rpg7_empty_zoom", stats=RPG7, model_path="auto")

