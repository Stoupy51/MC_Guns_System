
# Imports
from ..config.stats import PPSH41, add_item


# Main function should return a database
def main() -> None:

    # Add ppsh41
    add_item("ppsh41", stats=PPSH41, model_path="auto")
    add_item("ppsh41_zoom", stats=PPSH41, model_path="auto")

