
# Imports
from python_datapack.utils.database_helper import *


# Main function
def main(config: dict) -> None:
    ns: str = config["namespace"]
    version: str = config["version"]
    database: dict = config["database"]
    pass

    # Write to load file
    write_load_file(config, f"""
scoreboard objectives add {ns}.right_click
scoreboard objectives add {ns}.pending_clicks
""")

