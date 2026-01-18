
# Imports
from ..config.stats import TEMPLATE, add_item


# Main function should return a database
def main() -> None:

    # Add template
    add_item("template", stats=TEMPLATE, model_path="auto")
    add_item("template_zoom", stats=TEMPLATE, model_path="auto")
    add_item("template_1", stats=TEMPLATE, model_path="auto")
    add_item("template_1_zoom", stats=TEMPLATE, model_path="auto")
    add_item("template_2", stats=TEMPLATE, model_path="auto")
    add_item("template_2_zoom", stats=TEMPLATE, model_path="auto")
    add_item("template_3", stats=TEMPLATE, model_path="auto")
    add_item("template_3_zoom", stats=TEMPLATE, model_path="auto")
    add_item("template_4", stats=TEMPLATE, model_path="auto")
    add_item("template_4_zoom", stats=TEMPLATE, model_path="auto")

