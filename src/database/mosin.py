
# Imports
from ..config.stats import MOSIN, add_item


# Main function should return a database
def main() -> None:

    # Add mosin
    add_item("mosin", stats=MOSIN, model_path="auto")
    add_item("mosin_zoom", stats=MOSIN, model_path="auto")
    add_item("mosin_1", stats=MOSIN, model_path="auto")
    add_item("mosin_1_zoom", stats=MOSIN, model_path="auto")

