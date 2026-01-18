
# Imports
import os

from stewbeet import Item, Mem

# Variables
flash_models: list[str] = []
""" List storing all flash texture models that are loaded from the textures folder. """

# Main function should return a database
def main() -> None:
    ns: str = Mem.ctx.project_id

	# Get all "flash_X" in textures folder
    textures: list[str] = os.listdir(str(Mem.ctx.meta.get("stewbeet", {}).get("textures_folder", "")))
    flash_textures: list[str] = [f for f in textures if f.startswith("flash_")]

    # Add flashes to database
    for texture in flash_textures:
        model_name: str = texture.replace(".png", "")
        Item(
            id=model_name,
            base_item="minecraft:white_stained_glass_pane",
            override_model={
                "parent": "minecraft:item/white_stained_glass_pane",
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
        )
        flash_models.append(model_name)

