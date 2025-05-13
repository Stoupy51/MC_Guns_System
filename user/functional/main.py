
# Imports
from python_datapack.utils.database_helper import *

from user.config.blocks import main as write_block_tags


# Main function
def main(config: dict) -> None:
    ns: str = config["namespace"]
    version: str = config["version"]
    pass

    # Write to load file
    write_load_file(config,
f"""
# Define objectives
scoreboard objectives add {ns}.right_click minecraft.used:minecraft.warped_fungus_on_a_stick
scoreboard objectives add {ns}.pending_clicks dummy
scoreboard objectives add {ns}.cooldown dummy

# Define some constants
scoreboard players set #2 {ns}.data 2
scoreboard players set #10 {ns}.data 10
scoreboard players set #1000 {ns}.data 1000
scoreboard players set #1000000 {ns}.data 1000000
""", prepend=True)

    # Write to tick file
    write_tick_file(config,
f"""
# Player loop
execute as @a[sort=random] at @s run function {ns}:v{version}/player/tick
""")

    # Add block tags
    write_block_tags(config)

    ## Setup special damage type
    write_damage_type(config, f"{ns}:bullet", stp.super_json_dump({"exhaustion": 0, "message_id": "player", "scaling": "when_caused_by_living_non_player"}))
    write_tags(config, "damage_type/bypasses_cooldown", stp.super_json_dump({"values":[f"{ns}:bullet"]}))
    write_tags(config, "damage_type/no_knockback",      stp.super_json_dump({"values":[f"{ns}:bullet"]}))
    write_versioned_function(config, "utils/damage", f"$damage $(target) $(amount) {ns}:bullet by $(attacker)\n$say $(amount) by $(attacker)")

