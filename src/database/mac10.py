
# Imports
from ..config.stats import MAC10, add_item


# Main function should return a database
def main() -> None:

    # Add mac10
    add_item("mac10", stats=MAC10, model_path="auto")
    add_item("mac10_zoom", stats=MAC10, model_path="auto")

