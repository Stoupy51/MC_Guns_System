
# Imports
from stewbeet import (
    DamageType,
    Font,
    Mem,
    Texture,
    set_json_encoder,
    texture_mcmeta,
    write_load_file,
    write_tag,
    write_tick_file,
    write_versioned_function,
)

from ..config.blocks import main as write_block_tags
from ..config.stats import REMAINING_BULLETS


# Main function
def main() -> None:
    ns: str = Mem.ctx.project_id
    version: str = Mem.ctx.project_version

    # Write to load file
    write_load_file(
f"""
## Define objectives
# Detect right click with a gun (Alternative for weapon switching cooldown)
scoreboard objectives add {ns}.right_click minecraft.used:minecraft.warped_fungus_on_a_stick
scoreboard objectives add {ns}.alt_right_click minecraft.used:minecraft.carrot_on_a_stick
scoreboard objectives add {ns}.previous_selected dummy

# Tracks right clicks to enable continuous right-click detection
scoreboard objectives add {ns}.pending_clicks dummy

# Cooldown in ticks before being able to shot
scoreboard objectives add {ns}.cooldown dummy

# Indicates if the player was zooming (used to remove slowness)
scoreboard objectives add {ns}.zoom dummy

# Tracks the most recently selected weapon ID for weapon switching mechanics
scoreboard objectives add {ns}.last_selected dummy

# Tracks the current amount of bullets in the selected weapon
scoreboard objectives add {ns}.{REMAINING_BULLETS} dummy

# Tracks the room acoustics level for crack sound effects
scoreboard objectives add {ns}.acoustics_level dummy


# Define some constants
scoreboard players set #2 {ns}.data 2
scoreboard players set #10 {ns}.data 10
scoreboard players set #1000 {ns}.data 1000
scoreboard players set #1000000 {ns}.data 1000000
""", prepend=True)

    # Write to tick file
    write_tick_file(
f"""
# Player loop
execute as @a[sort=random] at @s run function {ns}:v{version}/player/tick
""")

    # Add block tags
    write_block_tags()

    ## Setup special damage type
    Mem.ctx.data[ns].damage_type["bullet"] = set_json_encoder(DamageType({"exhaustion": 0, "message_id": "player", "scaling": "when_caused_by_living_non_player"}))
    for tag in ["bypasses_cooldown", "no_knockback"]:
        write_tag(tag, Mem.ctx.data["minecraft"].damage_type_tags, [f"{ns}:bullet"])
    write_versioned_function("utils/damage", f"""
$damage $(target) $(amount) {ns}:bullet by $(attacker)
#$say damage $(target) $(amount) {ns}:bullet by $(attacker)
""")

    # Copy crosshair texture
    textures_folder: str = Mem.ctx.meta.get("stewbeet", {}).get("textures_folder", "")
    Mem.ctx.assets["minecraft"].textures["gui/sprites/hud/crosshair"] = Texture(source_path=f"{textures_folder}/crosshair.png") # type: ignore

    # Add bullet font (for actionbar)
    font: Font = Mem.ctx.assets.fonts.setdefault(f"{ns}:icons", Font({"providers": []}))
    font.data["providers"].extend([
        {"type": "bitmap","file": f"{ns}:font/bullet_full.png","ascent": 7,"height": 9,"chars": ["A"]},
        {"type": "bitmap","file": f"{ns}:font/bullet_outline.png","ascent": 7,"height": 9,"chars": ["B"]},
    ])
    for icon_name in ["bullet_outline", "bullet_full"]:
        Mem.ctx.assets[ns].textures[f"font/{icon_name}"] = texture_mcmeta(f"{textures_folder}/{icon_name}.png")

