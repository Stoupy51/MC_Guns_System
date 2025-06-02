
# Imports
from user.functional.main import main as main_datapack
from user.functional.tick import main as main_tick
from user.functional.weapon import main as main_weapon


# Main function is run just before making finalyzing the build process (zip, headers, lang, ...)
def main(config: dict) -> None:
    main_datapack(config)
    main_weapon(config)
    main_tick(config)

