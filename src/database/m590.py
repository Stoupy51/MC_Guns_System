
# Imports
from ..config.stats import M590, add_item


# Main function should return a database
def main() -> None:

    # Add m590
    add_item("m590", stats=M590, model_path="auto")
    add_item("m590_zoom", stats=M590, model_path="auto")
    add_item("m590_1", stats=M590, model_path="auto")
    add_item("m590_1_zoom", stats=M590, model_path="auto")
    add_item("m590_2", stats=M590, model_path="auto")
    add_item("m590_2_zoom", stats=M590, model_path="auto")
    add_item("m590_3", stats=M590, model_path="auto")
    add_item("m590_3_zoom", stats=M590, model_path="auto")

