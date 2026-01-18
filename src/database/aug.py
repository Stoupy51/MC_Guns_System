
# Imports
from ..config.stats import AUG, add_item


# Main function should return a database
def main() -> None:

    # Add aug
    add_item("aug", stats=AUG, model_path="auto")
    add_item("aug_zoom", stats=AUG, model_path="auto")
    add_item("aug_1", stats=AUG, model_path="auto")
    add_item("aug_1_zoom", stats=AUG, model_path="auto")
    add_item("aug_2", stats=AUG, model_path="auto")
    add_item("aug_2_zoom", stats=AUG, model_path="auto")
    add_item("aug_3", stats=AUG, model_path="auto")
    add_item("aug_3_zoom", stats=AUG, model_path="auto")
    add_item("aug_4", stats=AUG, model_path="auto")
    add_item("aug_4_zoom", stats=AUG, model_path="auto")

