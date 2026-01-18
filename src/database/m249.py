
# Imports
from ..config.stats import M249, add_item


# Main function should return a database
def main() -> None:

    # Add m249
    add_item("m249", stats=M249, model_path="auto")
    add_item("m249_zoom", stats=M249, model_path="auto")
    add_item("m249_1", stats=M249, model_path="auto")
    add_item("m249_1_zoom", stats=M249, model_path="auto")
    add_item("m249_2", stats=M249, model_path="auto")
    add_item("m249_2_zoom", stats=M249, model_path="auto")
    add_item("m249_3", stats=M249, model_path="auto")
    add_item("m249_3_zoom", stats=M249, model_path="auto")

