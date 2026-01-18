
# Imports
from ..config.stats import FAMAS, add_item


# Main function should return a database
def main() -> None:

    # Add famas
    add_item("famas", stats=FAMAS, model_path="auto")
    add_item("famas_zoom", stats=FAMAS, model_path="auto")
    add_item("famas_1", stats=FAMAS, model_path="auto")
    add_item("famas_1_zoom", stats=FAMAS, model_path="auto")
    add_item("famas_2", stats=FAMAS, model_path="auto")
    add_item("famas_2_zoom", stats=FAMAS, model_path="auto")
    add_item("famas_3", stats=FAMAS, model_path="auto")
    add_item("famas_3_zoom", stats=FAMAS, model_path="auto")
    add_item("famas_4", stats=FAMAS, model_path="auto")
    add_item("famas_4_zoom", stats=FAMAS, model_path="auto")

