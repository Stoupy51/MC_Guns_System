""" Zombies mode entry point; submodules run in dependency order. """
# Imports
from .common import ZombiesCommon
from .display_helpers import generate_display_helpers
from .enemies.escort import generate_zombies_escort
from .enemies.monkey_bomb import generate_monkey_bomb
from .enemies.roaming import generate_roaming
from .game.lifecycle import generate_zombies_game
from .game.round import generate_zombies_rounds
from .machines.mystery_box import generate_mystery_box
from .machines.pap import generate_pap
from .machines.perks import generate_perks
from .machines.wunderfizz import generate_wunderfizz
from .maps import generate_zombies_maps
from .menus import generate_zombies_menus
from .objects.barriers import generate_barriers
from .objects.doors import generate_doors
from .objects.power import generate_power_switch
from .objects.traps import generate_traps
from .objects.wallbuys import generate_wallbuys
from .player.ability import generate_zombies_abilities
from .player.hurt import generate_hurt_player
from .player.inventory import generate_zombies_inventory
from .player.revive import generate_revive
from .player.whos_who import generate_whos_who
from .rewards.bonus import main as bonus_main
from .rewards.powerups import generate_powerups


# Functions
def main() -> None:
	# Run all zombies modules
	ZombiesCommon.write_deny_functions()
	bonus_main()
	generate_zombies_maps()
	generate_zombies_menus()
	generate_zombies_game()
	generate_zombies_rounds()
	generate_zombies_escort()
	generate_zombies_abilities()
	generate_zombies_inventory()
	generate_display_helpers()
	generate_roaming()
	generate_mystery_box()
	generate_monkey_bomb()
	generate_pap()
	generate_barriers()
	generate_powerups()
	generate_power_switch()
	generate_doors()
	generate_wallbuys()
	generate_perks()
	generate_wunderfizz()
	generate_whos_who()
	generate_revive()
	generate_traps()
	generate_hurt_player()

