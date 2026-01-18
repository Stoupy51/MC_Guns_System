
# Imports
from ..config.stats import STEN, add_item


# Main function should return a database
def main() -> None:

    # Add sten
    add_item("sten", stats=STEN, model_path="auto")
    add_item("sten_zoom", stats=STEN, model_path="auto")

