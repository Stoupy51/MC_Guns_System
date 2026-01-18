
# Imports
from ..config.stats import SPAS12, add_item


# Main function should return a database
def main() -> None:

    # Add spas12
    add_item("spas12", stats=SPAS12, model_path="auto")
    add_item("spas12_zoom", stats=SPAS12, model_path="auto")
    add_item("spas12_1", stats=SPAS12, model_path="auto")
    add_item("spas12_1_zoom", stats=SPAS12, model_path="auto")
    add_item("spas12_2", stats=SPAS12, model_path="auto")
    add_item("spas12_2_zoom", stats=SPAS12, model_path="auto")
    add_item("spas12_3", stats=SPAS12, model_path="auto")
    add_item("spas12_3_zoom", stats=SPAS12, model_path="auto")

