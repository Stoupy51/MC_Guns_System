
# Imports
from user.functional.main import main as main_datapack
from user.functional.right_click import main as main_right_click
from user.functional.tick import main as main_tick


# Main function is run just before making finalyzing the build process (zip, headers, lang, ...)
def main(config: dict) -> None:
    main_datapack(config)
    main_right_click(config)
    main_tick(config)

