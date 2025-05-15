
# Imports
from python_datapack.utils.database_helper import write_versioned_function


# Main function
def main(config: dict) -> None:
    ns: str = config["namespace"]
    version: str = config["version"]

    # Handle pending clicks
    write_versioned_function(config, "player/right_click",
f"""
# Handle remaining ammo
function {ns}:v{version}/ammo/main
""")

    # Main function
    write_versioned_function(config, "ammo/main",
"""
# scoreboard players set ak47_mag S 30           # TODO: Not Implemented
# scoreboard players set ak47_reload S 70        # TODO: Not Implemented
# scoreboard players set ak47_reload_end S 10    # TODO: Not Implemented
""")

