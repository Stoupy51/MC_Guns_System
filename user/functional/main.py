
# Imports
from python_datapack.utils.database_helper import *

from user.config.blocks import main as write_block_tags


# Main function
def main(config: dict) -> None:
    ns: str = config["namespace"]
    version: str = config["version"]
    pass

    # Write to load file
    write_load_file(config, f"""
# Define objectives
scoreboard objectives add {ns}.right_click minecraft.used:minecraft.warped_fungus_on_a_stick
scoreboard objectives add {ns}.pending_clicks dummy
""", prepend=True)

    # Write to tick file
    write_tick_file(config, f"""
# Player loop
execute as @a[sort=random] at @s run function {ns}:v{version}/player/tick
""")

    # Add block tags
    write_block_tags(config)

