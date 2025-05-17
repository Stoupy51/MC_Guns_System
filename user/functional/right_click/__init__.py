
# Imports
from .ammo import main as ammo_main
from .casing import main as casing_main
from .common import main as common_main
from .kick import main as kick_main
from .raycast import main as raycast_main
from .sound import main as sound_main
from .zoom import main as zoom_main


# Main function
def main(config: dict) -> None:

    # Detect right click base
    common_main(config)

    # Handle zoom functionality
    zoom_main(config)

    # Handle shoot with raycast, with accuracy groups
    raycast_main(config)

    # Make a weapon kick
    kick_main(config)

    # Visually drop a casing
    casing_main(config)

    # All ammo logic
    ammo_main(config)

    # Advanced sound system
    sound_main(config)

