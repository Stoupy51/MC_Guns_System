
# Imports
from ..config.stats import M500, add_item


# Main function should return a database
def main() -> None:

    # Add m500
    add_item("m500", stats=M500, model_path="auto")
    add_item("m500_zoom", stats=M500, model_path="auto")
    add_item("m500_1", stats=M500, model_path="auto")
    add_item("m500_1_zoom", stats=M500, model_path="auto")
    add_item("m500_2", stats=M500, model_path="auto")
    add_item("m500_2_zoom", stats=M500, model_path="auto")
    add_item("m500_3", stats=M500, model_path="auto")
    add_item("m500_3_zoom", stats=M500, model_path="auto")

