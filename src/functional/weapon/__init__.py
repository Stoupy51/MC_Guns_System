
# Imports
from .ammo import main as ammo_main
from .casing import main as casing_main
from .common import main as common_main
from .flash import main as flash_main
from .kick import main as kick_main
from .raycast import main as raycast_main
from .sound import main as sound_main
from .switch import main as switch_main
from .zoom import main as zoom_main


# Main function
def main() -> None:

    # Detect right click base
    common_main()

    # Handle zoom functionality
    zoom_main()

    # Handle weapon switching mechanics
    switch_main()

    # Handle shoot with raycast, with accuracy groups
    raycast_main()

    # Make a weapon kick
    kick_main()

    # Visually drop a casing
    casing_main()

    # All ammo logic
    ammo_main()

    # Advanced sound system
    sound_main()

    # Handle flash effect when shooting
    flash_main()

