
# Imports
from .ability import generate_zombies_abilities
from .bonus import main as bonus_main
from .display_helpers import generate_display_helpers
from .doors import generate_doors
from .feedback import generate_zombies_feedback
from .game import generate_zombies_game
from .inventory import generate_zombies_inventory
from .maps import generate_zombies_maps
from .menus import generate_zombies_menus
from .mystery_box import generate_mystery_box
from .pap import generate_pap
from .perks import generate_perks
from .power import generate_power_switch
from .revive import generate_revive
from .round import generate_zombies_rounds
from .traps import generate_traps
from .wallbuys import generate_wallbuys


# Main function
def main() -> None:
    # Run all zombies modules
    bonus_main()
    generate_zombies_maps()
    generate_zombies_menus()
    generate_zombies_game()
    generate_zombies_rounds()
    generate_zombies_abilities()
    generate_zombies_feedback()
    generate_zombies_inventory()
    generate_display_helpers()
    generate_mystery_box()
    generate_pap()
    generate_power_switch()
    generate_doors()
    generate_wallbuys()
    generate_perks()
    generate_revive()
    generate_traps()

