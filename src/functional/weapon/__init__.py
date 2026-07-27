""" Weapon subsystem entry point; submodules run in dependency order. """
# Imports
from ..helpers.content import SharedContent
from .ammo.lore import main as update_lore_main
from .ammo.magazine import main as ammo_main
from .ammo.switch import main as switch_main
from .common import main as common_main
from .firing.casing import main as casing_main
from .firing.kick import main as kick_main
from .firing.left_click import main as left_click_main
from .firing.projectile import main as projectile_main
from .firing.raycast import main as raycast_main
from .firing.sound import main as sound_main
from .grenade import main as grenade_main
from .hud.actionbar import main as actionbar_main
from .hud.hit_indicator import main as hit_indicator_main
from .hud.zoom import main as zoom_main


# Functions
def main() -> None:
	SharedContent.write_shared_projectile_functions()  # Shared by the projectile and grenade systems
	common_main()                        # Right-click detection
	left_click_main()                    # Left-click (reload), via the piercing-attack enchantment
	zoom_main()
	switch_main()
	raycast_main()                       # Hitscan shots with accuracy groups
	projectile_main()                    # Slow projectiles (RPG rockets, etc.)
	grenade_main()
	kick_main()
	casing_main()
	ammo_main()
	actionbar_main()                     # Fire mode + ammo display
	update_lore_main()                   # Rebuild item lore from stats
	sound_main()
	hit_indicator_main()

