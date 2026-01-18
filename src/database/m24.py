
# Imports
from ..config.stats import M24, add_item


# Main function should return a database
def main() -> None:

    # Add m24
    add_item("m24", stats=M24, model_path="auto")
    add_item("m24_zoom", stats=M24, model_path="auto")
    add_item("m24_1", stats=M24, model_path="auto")
    add_item("m24_1_zoom", stats=M24, model_path="auto")
    add_item("m24_2", stats=M24, model_path="auto")
    add_item("m24_2_zoom", stats=M24, model_path="auto")
    add_item("m24_3", stats=M24, model_path="auto")
    add_item("m24_3_zoom", stats=M24, model_path="auto")
    add_item("m24_4", stats=M24, model_path="auto")
    add_item("m24_4_zoom", stats=M24, model_path="auto")

