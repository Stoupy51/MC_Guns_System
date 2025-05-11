
# Imports
from user.functional.right_click import main as main_right_click


# Main function is run just before making finalyzing the build process (zip, headers, lang, ...)
def main(config: dict) -> None:
    main_right_click(config)

