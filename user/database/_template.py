
# ruff: noqa: E501
# Imports
from user.config.stats import TEMPLATE, get_data


# Main function should return a database
def main(db: dict, ns: str) -> None:

    # Add template
    db["template"] = get_data(ns, TEMPLATE, {})
    db["template_zoom"] = get_data(ns, TEMPLATE, {})
    db["template_1"] = get_data(ns, TEMPLATE, {})
    db["template_1_zoom"] = get_data(ns, TEMPLATE, {})
    db["template_2"] = get_data(ns, TEMPLATE, {})
    db["template_2_zoom"] = get_data(ns, TEMPLATE, {})
    db["template_3"] = get_data(ns, TEMPLATE, {})
    db["template_3_zoom"] = get_data(ns, TEMPLATE, {})
    db["template_4"] = get_data(ns, TEMPLATE, {})
    db["template_4_zoom"] = get_data(ns, TEMPLATE, {})

