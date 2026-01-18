
# Imports
from ..config.stats import RPK, add_item


# Main function should return a database
def main() -> None:

    # Add rpk
    add_item("rpk", stats=RPK, model_path="auto")
    add_item("rpk_zoom", stats=RPK, model_path="auto")
    add_item("rpk_1", stats=RPK, model_path="auto")
    add_item("rpk_1_zoom", stats=RPK, model_path="auto")
    add_item("rpk_2", stats=RPK, model_path="auto")
    add_item("rpk_2_zoom", stats=RPK, model_path="auto")
    add_item("rpk_3", stats=RPK, model_path="auto")
    add_item("rpk_3_zoom", stats=RPK, model_path="auto")
    add_item("rpk_4", stats=RPK, model_path="auto")
    add_item("rpk_4_zoom", stats=RPK, model_path="auto")

