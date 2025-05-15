
# Imports
from python_datapack.utils.database_helper import write_versioned_function


# Main function
def main(config: dict) -> None:
    ns: str = config["namespace"]
    version: str = config["version"]

    # Handle pending clicks
    write_versioned_function(config, "player/right_click",
f"""
# Advanced Playsound
function {ns}:v{version}/sound/main
""")

    # Main function
    write_versioned_function(config, "sound/main",
f"""
# TODO: Advanced playsound using cracks and stuff
playsound {ns}:ak47/fire player @s ~ ~1000000 ~ 400000
playsound {ns}:ak47/fire player @a[distance=0.01..48] ~ ~ ~ 3
""")

