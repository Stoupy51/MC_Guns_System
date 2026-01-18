
# Imports
from ..config.stats import FNFAL, add_item


# Main function should return a database
def main() -> None:

    # Add fnfal
    add_item("fnfal", stats=FNFAL, model_path="auto")
    add_item("fnfal_zoom", stats=FNFAL, model_path="auto")
    add_item("fnfal_1", stats=FNFAL, model_path="auto")
    add_item("fnfal_1_zoom", stats=FNFAL, model_path="auto")
    add_item("fnfal_2", stats=FNFAL, model_path="auto")
    add_item("fnfal_2_zoom", stats=FNFAL, model_path="auto")
    add_item("fnfal_3", stats=FNFAL, model_path="auto")
    add_item("fnfal_3_zoom", stats=FNFAL, model_path="auto")
    add_item("fnfal_4", stats=FNFAL, model_path="auto")
    add_item("fnfal_4_zoom", stats=FNFAL, model_path="auto")

