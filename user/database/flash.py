
# Imports
from typing import Any

from python_datapack.constants import OVERRIDE_MODEL

# Variables
flash_models: list[str] = []
""" List storing all flash texture models that are loaded from the textures folder. """

# Main function should return a database
def main(config: dict[str, Any], database: dict[str, Any]) -> None:
    ns: str = config["namespace"]

	# Get all "flash_X" in textures folder
    textures: str = config["textures_files"]
    flash_textures: list[str] = [f for f in textures if f.startswith("flash_")]

    # Add flashes to database
    for texture in flash_textures:
        model_name: str = texture.replace(".png", "")
        database[model_name] = {
            "id": "minecraft:white_stained_glass_pane",
            OVERRIDE_MODEL: {
                "textures": {
                    "layer0": f"{ns}:item/{model_name}"
                },
                "elements": [
                    {
                        "from": [0, 0, 8],
                        "to": [16, 16, 8],
                        "light_emission": 15,
                        "shade": False,
                        "rotation": {"angle": 0, "axis": "y", "origin": [0, 0, 8]},
                        "faces": {
                            "north": {"uv": [0, 0, 16, 16], "texture": "#layer0"},
                            "east": {"uv": [8, 0, 8, 16], "texture": "#layer0"},
                            "south": {"uv": [0, 0, 16, 16], "texture": "#layer0"},
                            "west": {"uv": [8, 0, 8, 16], "texture": "#layer0"},
                            "up": {"uv": [0, 8, 16, 8], "texture": "#layer0"},
                            "down": {"uv": [0, 8, 16, 8], "texture": "#layer0"}
                        }
                    }
                ]
            }
        }
        flash_models.append(model_name)

