
# Imports
from python_datapack.utils.database_helper import write_versioned_function

from user.config.stats import *


# Main function
def main(config: dict) -> None:
    ns: str = config["namespace"]
    version: str = config["version"]

    # Handle pending clicks
    write_versioned_function(config, "player/right_click",
f"""
# Drop casing
function {ns}:v{version}/casing/main
""")

    # Main function
    write_versioned_function(config, "casing/main",
"""
# TODO: Casing
# scoreboard players set ak47_casing_n S 200     # TODO: Not Implemented
# scoreboard players set ak47_casing_t S 50      # TODO: Not Implemented
# scoreboard players set ak47_casing_b S -200    # TODO: Not Implemented
""")

