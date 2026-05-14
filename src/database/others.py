
# Imports
from stewbeet import Item

from ..config.stats import get_model_path, load_model


# Main function should return a database
def main() -> None:

    # Add Pack-a-Punch
    Item(id="pack_a_punch", override_model=load_model(get_model_path("pack_a_punch")))

