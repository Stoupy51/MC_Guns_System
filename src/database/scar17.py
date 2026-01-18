
# Imports
from ..config.stats import SCAR17, add_item


# Main function should return a database
def main() -> None:

    # Add scar17
    add_item("scar17", stats=SCAR17, model_path="auto")
    add_item("scar17_zoom", stats=SCAR17, model_path="auto")
    add_item("scar17_1", stats=SCAR17, model_path="auto")
    add_item("scar17_1_zoom", stats=SCAR17, model_path="auto")
    add_item("scar17_2", stats=SCAR17, model_path="auto")
    add_item("scar17_2_zoom", stats=SCAR17, model_path="auto")
    add_item("scar17_3", stats=SCAR17, model_path="auto")
    add_item("scar17_3_zoom", stats=SCAR17, model_path="auto")
    add_item("scar17_4", stats=SCAR17, model_path="auto")
    add_item("scar17_4_zoom", stats=SCAR17, model_path="auto")

