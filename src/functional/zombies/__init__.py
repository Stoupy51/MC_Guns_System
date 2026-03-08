
# Imports
from .bonus import main as bonus_main
from .game import generate_zombies_game
from .maps import generate_zombies_maps
from .menus import generate_zombies_menus
from .mystery_box import generate_mystery_box


# Main function
def main() -> None:
    # Run all zombies modules
    bonus_main()
    generate_zombies_maps()
    generate_zombies_menus()
    generate_zombies_game()
    generate_mystery_box()

